from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import ExpenseListCreateView
from .views_ai import ForecastView, NLQueryView, SuggestBudgetView
from .views_auth import ProfileView, RegisterView
from .views_extra import BudgetListCreateView, CategoryListCreateView
from .views_reports import MonthlyCategoryReportView

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("expenses/", ExpenseListCreateView.as_view(), name="expenses"),
    path("categories/", CategoryListCreateView.as_view(), name="categories"),
    path("budgets/", BudgetListCreateView.as_view(), name="budgets"),
    path(
        "reports/monthly/",
        MonthlyCategoryReportView.as_view(),
        name="monthly_report",
    ),
    path(
        "ai/suggest-budget/",
        SuggestBudgetView.as_view(),
        name="suggest_budget",
    ),
    path("ai/forecast/", ForecastView.as_view(), name="forecast"),
    path("ai/query/", NLQueryView.as_view(), name="nl_query"),
]
