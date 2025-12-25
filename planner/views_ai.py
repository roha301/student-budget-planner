from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.throttling import SimpleRateThrottle
from django.db.models import Sum
from .models import Expense
from .openai_client import OpenAIClient
from .serializers_ai import (
    SuggestBudgetRequestSerializer,
    ForecastRequestSerializer,
    NLQueryRequestSerializer,
)

class AILimitThrottle(SimpleRateThrottle):
    scope = 'ai'
    rate = '10/hour'

    def get_cache_key(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return None
        return self.cache_format % {
            'scope': self.scope,
            'ident': request.user.pk
        }

class _UserHistoryHelper:
    @staticmethod
    def build_summary(user, months=3):
        qs = Expense.objects.filter(user=user).order_by('-date')[:months * 30]
        # build simple summary: totals per category and recent items
        totals = (
            Expense.objects.filter(user=user)
            .values('category__name')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )
        top = [{ 'category': t['category__name'] or 'Uncategorized', 'total': float(t['total'] or 0)} for t in totals]
        recent = list(qs.values('description', 'amount', 'date')[:20])
        summary = f"Top categories: {top}\nRecent items: {recent}"
        return summary

class SuggestBudgetView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AILimitThrottle]

    def post(self, request):
        ser = SuggestBudgetRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        months = ser.validated_data.get('months_of_history', 3)
        summary = _UserHistoryHelper.build_summary(request.user, months)
        res = OpenAIClient.suggest_budget(summary)
        if 'error' in res:
            return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(res)

class ForecastView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AILimitThrottle]

    def post(self, request):
        ser = ForecastRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        months = ser.validated_data.get('months', 3)
        summary = _UserHistoryHelper.build_summary(request.user, months)
        res = OpenAIClient.forecast_expenses(summary, months=months)
        if 'error' in res:
            return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(res)

class NLQueryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [AILimitThrottle]

    def post(self, request):
        ser = NLQueryRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        query = ser.validated_data['query']
        summary = _UserHistoryHelper.build_summary(request.user, months=6)
        res = OpenAIClient.answer_nl_query(summary, query)
        if 'error' in res:
            return Response(res, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(res)
