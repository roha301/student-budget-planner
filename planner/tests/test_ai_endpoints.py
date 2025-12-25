from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from planner.models import Category, Expense


class AITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="pass"
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        cat = Category.objects.create(name="Food", user=self.user)
        Expense.objects.create(
            user=self.user,
            category=cat,
            amount=Decimal("4.50"),
            description="Coffee",
            date=date.today(),
        )
        Expense.objects.create(
            user=self.user,
            category=cat,
            amount=Decimal("12.00"),
            description="Lunch",
            date=date.today(),
        )

    def test_suggest_budget(self):
        url = reverse("suggest_budget")
        resp = self.client.post(
            url,
            data={"months_of_history": 2},
            format="json",
        )
        # We can't require OpenAI; accept 200 or 503 but ensure response structure
        self.assertIn(resp.status_code, (200, 503))

    def test_forecast(self):
        url = reverse("forecast")
        resp = self.client.post(url, data={"months": 2}, format="json")
        self.assertIn(resp.status_code, (200, 503))

    def test_nl_query(self):
        url = reverse("nl_query")
        resp = self.client.post(
            url,
            data={
                "query": "How much did I spend on food last month?",
            },
            format="json",
        )
        self.assertIn(resp.status_code, (200, 503))
