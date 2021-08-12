from rest_framework.generics import ListAPIView

from api.apps.problems.models import Question
from api.apps.problems.serializers import QuestionSerializer


class QuestionsList(ListAPIView):
    queryset = Question.objects.all_with_fk()
    serializer_class = QuestionSerializer
