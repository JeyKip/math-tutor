from rest_framework.generics import RetrieveAPIView

from api.apps.problems.models import Question
from api.apps.problems.serializers import QuestionWithOptionsSerializer


class QuestionDetails(RetrieveAPIView):
    queryset = Question.objects.all_with_fk_and_many()
    serializer_class = QuestionWithOptionsSerializer
