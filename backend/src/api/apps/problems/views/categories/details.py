from rest_framework.generics import RetrieveAPIView

from api.apps.problems.models import Category
from api.apps.problems.serializers import CategorySerializer


class CategoryDetails(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
