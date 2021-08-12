from django.urls import path, reverse

from api.apps.problems.views.categories import CategoriesList, CategoryDetails
from api.apps.problems.views.questions import QuestionsList, QuestionDetails

app_name = "problems"
categories_list_name = "categories-list"
category_details_url_name = "category-details"
questions_list_name = "questions-list"
question_details_url_name = "question-details"

urlpatterns = [
    path('categories/', CategoriesList.as_view(), name=categories_list_name),
    path('categories/<pk>/', CategoryDetails.as_view(), name=category_details_url_name),
    path('questions/', QuestionsList.as_view(), name=questions_list_name),
    path('questions/<pk>/', QuestionDetails.as_view(), name=question_details_url_name),
]


class ProblemsAppUrls:
    @staticmethod
    def categories_list_url():
        return reverse(f"{app_name}:{categories_list_name}")

    @staticmethod
    def category_details_url(pk):
        return reverse(f"{app_name}:{category_details_url_name}", kwargs={'pk': pk})

    @staticmethod
    def questions_list_url():
        return reverse(f"{app_name}:{questions_list_name}")

    @staticmethod
    def question_details_url(pk):
        return reverse(f"{app_name}:{question_details_url_name}", kwargs={'pk': pk})
