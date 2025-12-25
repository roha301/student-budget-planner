from django.urls import path
from .views import ExpenseListCreateView
from .views_extra import CategoryListCreateView, BudgetListCreateView
from .views_reports import MonthlyCategoryReportView
from .views_ai import SuggestBudgetView, ForecastView, NLQueryView
from .views_auth import RegisterView, ProfileView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expenses'),
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('budgets/', BudgetListCreateView.as_view(), name='budgets'),
    path('reports/monthly/', MonthlyCategoryReportView.as_view(), name='monthly_report'),
    path('ai/suggest-budget/', SuggestBudgetView.as_view(), name='suggest_budget'),
    path('ai/forecast/', ForecastView.as_view(), name='forecast'),
    path('ai/query/', NLQueryView.as_view(), name='nl_query'),
]
