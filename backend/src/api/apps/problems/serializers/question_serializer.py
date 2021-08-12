from rest_framework import serializers

from api.apps.problems.models import Question
from .category_serializer import CategorySerializer
from .option_serializer import OptionSerializer


class QuestionSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    question = serializers.CharField(max_length=2048, source="text")

    class Meta:
        model = Question
        fields = ("id", "category", "type", "question", "complexity", "number_of_points", "max_attempts_to_solve")


class QuestionWithOptionsSerializer(QuestionSerializer):
    options = OptionSerializer(many=True)

    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ("options",)
