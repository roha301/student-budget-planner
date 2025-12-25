from rest_framework import generics, permissions

from .models import Category, Expense
from .openai_client import OpenAIClient
from .serializers import ExpenseSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Expense.objects.filter(user=user).order_by("-date")
        return Expense.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        description = serializer.validated_data.get("description", "")
        category_obj = None
        if description:
            res = OpenAIClient.categorize_expense(description)
            cat_name = res.get("category") if isinstance(res, dict) else res
            if cat_name:
                category_obj, _ = Category.objects.get_or_create(
                    name=cat_name, user=user
                )
        serializer.save(user=user, category=category_obj)
