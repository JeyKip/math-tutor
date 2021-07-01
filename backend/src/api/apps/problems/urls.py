from django.urls import path, reverse

from api.apps.problems.views.categories import CategoriesList, CategoryDetails

app_name = "problems"
categories_list_name = "categories-list"
category_details_url_name = "category-details"

urlpatterns = [
    path('categories/', CategoriesList.as_view(), name=categories_list_name),
    path('categories/<pk>/', CategoryDetails.as_view(), name=category_details_url_name)
]


class ProblemsAppUrls:
    @staticmethod
    def list_url():
        return reverse(f"{app_name}:{categories_list_name}")

    @staticmethod
    def details_url(pk):
        return reverse(f"{app_name}:{category_details_url_name}", kwargs={'pk': pk})
