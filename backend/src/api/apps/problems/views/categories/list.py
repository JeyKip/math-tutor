from rest_framework.generics import ListAPIView

from api.apps.problems.models import Category
from api.apps.problems.serializers import CategorySerializer


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
