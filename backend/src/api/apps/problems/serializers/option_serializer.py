from rest_framework import serializers

from api.apps.problems.models import Option


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ("id", "value")
