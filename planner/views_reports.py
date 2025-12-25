from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .db import call_get_monthly_spend


class MonthlyCategoryReportView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        year = int(request.query_params.get("year", 2025))
        month = int(request.query_params.get("month", 12))
        user = request.user
        data = call_get_monthly_spend(user.id, year, month)
        return Response({"year": year, "month": month, "data": data})
