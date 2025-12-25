from rest_framework import serializers


class SuggestBudgetSerializer(serializers.Serializer):
    suggestion = serializers.JSONField()


class ForecastSerializer(serializers.Serializer):
    forecasts = serializers.JSONField()


class NLQuerySerializer(serializers.Serializer):
    answer = serializers.CharField()
    followup = serializers.CharField(allow_blank=True, required=False)


class SuggestBudgetRequestSerializer(serializers.Serializer):
    months_of_history = serializers.IntegerField(default=3)


class ForecastRequestSerializer(serializers.Serializer):
    months = serializers.IntegerField(default=3)


class NLQueryRequestSerializer(serializers.Serializer):
    query = serializers.CharField()
