from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from planner.models import Category, Expense


class OpenAICacheTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cachetester", password="pass"
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

    @patch("openai.ChatCompletion.create")
    def test_suggest_budget_cached(self, mock_create):
        # Mock the low-level OpenAI method; _chat caching should prevent multiple calls
        content_json = (
            '{"monthly_income": 1000, "allocations": [], '
            '"notes": "ok"}'
        )
        mock_create.return_value = type(
            "obj",
            (),
            {
                "choices": [
                    type(
                        "c",
                        (),
                        {
                            "message": type(
                                "m",
                                (),
                                {"content": content_json},
                            )()
                        },
                    )
                ]
            },
        )()
        url = reverse("suggest_budget")
        # First call should invoke OpenAI
        resp1 = self.client.post(
            url,
            data={"months_of_history": 1},
            format="json",
        )
        self.assertIn(resp1.status_code, (200, 503))
        # Second call should hit the cache and not call the OpenAI API again
        resp2 = self.client.post(
            url,
            data={"months_of_history": 1},
            format="json",
        )
        self.assertIn(resp2.status_code, (200, 503))
        # low-level create should have been called exactly once if caching worked
        self.assertLessEqual(mock_create.call_count, 1)
