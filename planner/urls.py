from django.urls import path
from .views import ExpenseListCreateView
from .views_extra import CategoryListCreateView, BudgetListCreateView
from .views_reports import MonthlyCategoryReportView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expenses'),
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('budgets/', BudgetListCreateView.as_view(), name='budgets'),
    path('reports/monthly/', MonthlyCategoryReportView.as_view(), name='monthly_report'),
]
