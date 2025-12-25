from django.contrib import admin

from .models import Budget, Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "amount", "start_date", "end_date")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "date", "category")
    list_filter = ("date", "category")
