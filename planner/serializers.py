from rest_framework import serializers

from .models import Budget, Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "user",
            "category",
            "amount",
            "description",
            "date",
            "created_at",
        ]


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "user", "name", "amount", "start_date", "end_date"]
