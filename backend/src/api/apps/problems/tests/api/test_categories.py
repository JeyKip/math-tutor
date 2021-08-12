from django.test import TestCase

from api.apps.problems.models import Category
from api.apps.problems.tests.api.api_helper import ApiHelper
from api.apps.problems.urls import ProblemsAppUrls


class CategoriesTestCase(TestCase):
    def setUp(self) -> None:
        self.api_helper = ApiHelper()

    def test_no_categories_saved_empty_list_should_be_returned(self):
        response = self.client.get(ProblemsAppUrls.categories_list_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_categories_exist_all_categories_should_be_returned(self):
        algebra = self.api_helper.create_category("Algebra")
        geometry = self.api_helper.create_category("Geometry")

        response = self.client.get(ProblemsAppUrls.categories_list_url())
        algebra_from_response = self.__find_category_in_response(response, algebra.name)
        geometry_from_response = self.__find_category_in_response(response, geometry.name)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(algebra_from_response)
        self.assertIsNotNone(geometry_from_response)

    def test_find_by_not_existing_category_should_return_404(self):
        response = self.client.get(ProblemsAppUrls.category_details_url(0))

        self.assertEqual(response.status_code, 404)

    def test_find_by_existing_category_should_return_single_category(self):
        algebra = self.api_helper.create_category("Algebra")

        response = self.client.get(ProblemsAppUrls.category_details_url(algebra.id))
        algebra_from_response = Category(**response.json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(algebra_from_response.name, algebra.name)

    def __find_category_in_response(self, response, name):
        return Category(**[category for category in response.json() if category["name"] == name][0])
