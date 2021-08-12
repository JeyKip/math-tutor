from django.test import TestCase

from api.apps.problems.models import Question
from api.apps.problems.tests.api.api_helper import ApiHelper
from api.apps.problems.tests.api.converters import QuestionConverter
from api.apps.problems.tests.constants import SIMPLE_QUESTION_TYPES, COMPLEX_QUESTION_TYPES
from api.apps.problems.urls import ProblemsAppUrls


class QuestionsTestCase(TestCase):
    def setUp(self) -> None:
        self.api = ApiHelper()
        self.question_converter = QuestionConverter()

    def test_no_questions_saved_empty_list_should_be_returned(self):
        response = self.client.get(ProblemsAppUrls.questions_list_url())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_questions_list_all_questions_should_be_returned_without_options_and_correct_answers(self):
        all_questions = self.create_bunch_of_questions()

        response = self.client.get(ProblemsAppUrls.questions_list_url())
        expected_response = [
            self.question_converter.to_list_item(question)
            for question in all_questions
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response, response.data)

    def test_single_question_of_simple_type_options_should_be_empty_list(self):
        questions = [question for question in self.create_bunch_of_questions() if
                     question.type in SIMPLE_QUESTION_TYPES]

        expected_responses_data = [
            self.question_converter.to_item_details(question)
            for question in questions
        ]
        actual_responses_data = [
            self.client.get(ProblemsAppUrls.question_details_url(question.id)).data
            for question in questions
        ]

        self.assertEqual(len(actual_responses_data), len(SIMPLE_QUESTION_TYPES))
        self.assertEqual(expected_responses_data, actual_responses_data)

        # assert that for questions with simple types options list isn't filled
        self.assertTrue(all([
            "options" in response and len(response["options"]) == 0
            for response in actual_responses_data
        ]))

    def test_single_question_of_complex_type_options_should_be_filled(self):
        questions = [question for question in self.create_bunch_of_questions() if
                     question.type in COMPLEX_QUESTION_TYPES]

        expected_responses_data = [
            self.question_converter.to_item_details(question)
            for question in questions
        ]
        actual_responses_data = [
            self.client.get(ProblemsAppUrls.question_details_url(question.id)).data
            for question in questions
        ]

        self.assertEqual(len(actual_responses_data), len(COMPLEX_QUESTION_TYPES))
        self.assertEqual(expected_responses_data, actual_responses_data)

        # assert that for questions with complex types options list is filled
        self.assertTrue(all([
            "options" in response and len(response["options"]) > 0
            for response in actual_responses_data
        ]))

    def create_bunch_of_questions(self):
        algebra = self.api.create_category("Algebra")
        geometry = self.api.create_category("Geometry")

        integer_question = self.api.create_question(algebra, Question.QuestionType.INTEGER.value, "2+2=?", 4)
        decimal_question = self.api.create_question(geometry, Question.QuestionType.DECIMAL.value, "PI?", 3.14)
        boolean_question = self.api.create_question(algebra, Question.QuestionType.BOOLEAN.value,
                                                    "The logarithm is the inverse function to exponentiation.",
                                                    "Yes")
        text_question = self.api.create_question(algebra, Question.QuestionType.TEXT.value,
                                                 "What is the inverse function to exponentiation?",
                                                 "Logarithm")
        single_choice_question = self.api.create_question(geometry, Question.QuestionType.SINGLE_CHOICE.value,
                                                          "In a 30-60-90 triangle, the length of the hypotenuse is 6."
                                                          " What is the length of the shortest side?")
        self.api.create_option(single_choice_question, "2", False)
        self.api.create_option(single_choice_question, "3", True)

        multiple_choice_question = self.api.create_question(algebra, Question.QuestionType.MULTIPLE_CHOICE.value,
                                                            "Select correct statements")
        self.api.create_option(multiple_choice_question, "2+2=4", True)
        self.api.create_option(multiple_choice_question, "2*3=7", False)
        self.api.create_option(multiple_choice_question, "9*9=81", True)

        return (multiple_choice_question, single_choice_question, text_question, boolean_question, decimal_question,
                integer_question)
