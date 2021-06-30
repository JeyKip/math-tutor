from django.urls import path

from api.apps.problems.views.categories import CategoriesList, CategoryDetails

urlpatterns = [
    path('categories', CategoriesList.as_view()),
    path('categories/', CategoriesList.as_view()),
    path('categories/<pk>', CategoryDetails.as_view())
]
