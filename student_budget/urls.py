from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("planner.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "dashboard/",
        lambda request: render(request, "dashboard.html"),
        name="dashboard",
    ),
    path(
        "transactions/",
        lambda request: render(request, "expenses.html"),
        name="transactions",
    ),
    path(
        "login/",
        lambda request: render(request, "auth_login.html"),
        name="login",
    ),
    path(
        "register/",
        lambda request: render(request, "auth_register.html"),
        name="register",
    ),
]
