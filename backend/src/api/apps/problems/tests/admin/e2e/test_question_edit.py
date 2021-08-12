from collections import namedtuple
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui

from api.apps.problems.models import Category, Question
from .admin_e2e_base_test_case import AdminE2EBaseTestCase
from ...constants import SIMPLE_QUESTION_TYPES, COMPLEX_QUESTION_TYPES, ALL_QUESTION_TYPES

QuestionData = namedtuple("QuestionData", [
    "category_name",
    "question",
    "complexity",
    "number_of_points",
    "correct_answer",
    "max_attempts_to_solve",
    "solution",
    "options"
])

ElementsVisibility = namedtuple("ElementsVisibility", ["visible_elements", "invisible_elements"])

OptionData = namedtuple("OptionData", ["value", "correct"])


class QuestionEditTestCase(AdminE2EBaseTestCase):
    default_categories = [
        "Elementary Algebra",
        "Elementary Geometry",
        "Linear Algebra",
        "Calculus",
        "Probability Theory"
    ]
    category_block_locator = (By.CLASS_NAME, "field-category", "Category")
    category_element_id = "id_category"
    category_element_locator = (By.ID, category_element_id)

    question_block_locator = (By.CLASS_NAME, "field-text", "Question")
    question_element_id = "id_text"
    question_element_locator = (By.ID, question_element_id)

    type_block_locator = (By.CLASS_NAME, "field-type", "Type")
    type_element_id = "id_type"
    type_element_locator = (By.ID, type_element_id)

    complexity_block_locator = (By.CLASS_NAME, "field-complexity", "Complexity")
    complexity_element_id = "id_complexity"
    complexity_element_locator = (By.ID, complexity_element_id)

    number_of_points_block_locator = (By.CLASS_NAME, "field-number_of_points", "Number of Points")
    number_of_points_element_id = "id_number_of_points"
    number_of_points_element_locator = (By.ID, number_of_points_element_id)

    max_attempts_to_solve_block_locator = (By.CLASS_NAME, "field-max_attempts_to_solve", "Max Attempts To Solve")
    max_attempts_to_solve_element_id = "id_max_attempts_to_solve"
    max_attempts_to_solve_element_locator = (By.ID, max_attempts_to_solve_element_id)

    integer_correct_answer_block_locator = (By.CLASS_NAME, "field-integer_correct_answer", "Integer Correct Answer")
    integer_correct_answer_element_id = "id_integer_correct_answer"
    integer_correct_answer_element_locator = (By.ID, integer_correct_answer_element_id)

    decimal_correct_answer_block_locator = (By.CLASS_NAME, "field-decimal_correct_answer", "Decimal Correct Answer")
    decimal_correct_answer_element_id = "id_decimal_correct_answer"
    decimal_correct_answer_element_locator = (By.ID, decimal_correct_answer_element_id)

    boolean_correct_answer_block_locator = (By.CLASS_NAME, "field-boolean_correct_answer", "Boolean Correct Answer")
    boolean_correct_answer_element_id = "id_boolean_correct_answer"
    boolean_correct_answer_element_locator = (By.ID, boolean_correct_answer_element_id)

    text_correct_answer_block_locator = (By.CLASS_NAME, "field-text_correct_answer", "Text Correct Answer")
    text_correct_answer_element_id = "id_text_correct_answer"
    text_correct_answer_element_locator = (By.ID, text_correct_answer_element_id)

    solution_block_locator = (By.CLASS_NAME, "field-solution", "Solution")
    solution_element_id = "id_solution"
    solution_element_locator = (By.ID, solution_element_id)

    save_button_locator = (By.CSS_SELECTOR, ".submit-row [name=_save]")
    errornote_locator = (By.CLASS_NAME, "errornote", "Error note")
    options_locator = (By.ID, "options-group")
    add_new_option_locator = (By.CSS_SELECTOR, "#options-group tr.add-row a")
    new_option_row_locator = (By.CSS_SELECTOR, "#options-group tbody tr.form-row.dynamic-options:nth-last-child(3)")

    elements_visibility_by_type = {
        Question.QuestionType.INTEGER.value: ElementsVisibility(
            [integer_correct_answer_block_locator],
            [decimal_correct_answer_block_locator, boolean_correct_answer_block_locator,
             text_correct_answer_block_locator, options_locator]
        ),
        Question.QuestionType.DECIMAL.value: ElementsVisibility(
            [decimal_correct_answer_block_locator],
            [integer_correct_answer_block_locator, boolean_correct_answer_block_locator,
             text_correct_answer_block_locator, options_locator]
        ),
        Question.QuestionType.BOOLEAN.value: ElementsVisibility(
            [boolean_correct_answer_block_locator],
            [integer_correct_answer_block_locator, decimal_correct_answer_block_locator,
             text_correct_answer_block_locator, options_locator]
        ),
        Question.QuestionType.TEXT.value: ElementsVisibility(
            [text_correct_answer_block_locator],
            [integer_correct_answer_block_locator, decimal_correct_answer_block_locator,
             boolean_correct_answer_block_locator, options_locator]
        ),
        Question.QuestionType.SINGLE_CHOICE.value: ElementsVisibility(
            [options_locator],
            [integer_correct_answer_block_locator, decimal_correct_answer_block_locator,
             boolean_correct_answer_block_locator, text_correct_answer_block_locator]
        ),
        Question.QuestionType.MULTIPLE_CHOICE.value: ElementsVisibility(
            [options_locator],
            [integer_correct_answer_block_locator, decimal_correct_answer_block_locator,
             boolean_correct_answer_block_locator, text_correct_answer_block_locator]
        )
    }

    default_integer_question_data = QuestionData("Elementary Algebra", "2+2=?", Question.Complexity.EASY.value, 1, 4,
                                                 None, None, None)
    default_decimal_question_data = QuestionData("Elementary Algebra", "9/2=?", Question.Complexity.EASY.value, 1, 4.5,
                                                 None, None, None)
    default_boolean_question_data = QuestionData("Elementary Algebra",
                                                 "The logarithm is the inverse function to exponentiation.",
                                                 Question.Complexity.MEDIUM.value, 2, "Yes", None, None, None)
    default_text_question_data = QuestionData("Elementary Algebra", "What is the inverse function to exponentiation?",
                                              Question.Complexity.MEDIUM.value, 1, "Logarithm", None, None, None)
    default_single_choice_question_data = \
        QuestionData("Elementary Algebra", "2+2=?", Question.Complexity.EASY.value, 1, None, None, None,
                     [OptionData("2+2=4", True), OptionData("2+5=6", False)])
    default_multiple_choice_question_data = \
        QuestionData("Elementary Algebra", "Select correct statements", Question.Complexity.EASY.value, 1, None, None,
                     None, [OptionData("2+2=4", True), OptionData("2+5=6", False), OptionData("9*9=81", True)])

    def test_default_view_of_add_question_page(self):
        self.open_add_question_page()

        self.assertVisible(self.category_block_locator)
        self.assertVisible(self.question_block_locator)
        self.assertVisible(self.type_block_locator)
        self.assertVisible(self.complexity_block_locator)
        self.assertVisible(self.number_of_points_block_locator)
        self.assertVisible(self.max_attempts_to_solve_block_locator)
        self.assertVisible(self.solution_block_locator)

        self.assertInvisible(self.integer_correct_answer_block_locator)
        self.assertInvisible(self.decimal_correct_answer_block_locator)
        self.assertInvisible(self.boolean_correct_answer_block_locator)
        self.assertInvisible(self.text_correct_answer_block_locator)
        self.assertInvisible(self.options_locator)

    def test_category_field_should_be_required_select_with_empty_option_selected_by_default(self):
        self.open_add_question_page()

        category_element = self.find_element(self.category_element_locator)

        self.assertSelectTag(category_element)
        self.assertValueEmpty(category_element)
        self.assertRequired(category_element)
        self.assertLabelForFieldMarkedRequired(self.category_element_id)

        # check that if there are no categories added yet category select box should show one empty option by default
        expected_options = {("", "---------")}
        actual_options = set(
            [(option.get_attribute("value"), option.text) for option in ui.Select(category_element).options])

        self.assertEqual(expected_options, actual_options)

    def test_category_select_should_be_fulfilled_with_all_categories(self):
        self.create_default_categories()
        self.open_add_question_page()

        category_select = self.find_category_select()

        expected_options = set(["---------"] + self.default_categories)
        actual_options = set([option.text for option in category_select.options])

        self.assertEqual(expected_options, actual_options)

    # noinspection DuplicatedCode
    def test_question_field_should_be_required_textarea_with_empty_text_by_default(self):
        self.open_add_question_page()

        question_element = self.find_element(self.question_element_locator)

        self.assertTextareaTag(question_element)
        self.assertTextEmpty(question_element)
        self.assertAttributeEqual(question_element, "rows", "10")
        self.assertAttributeEqual(question_element, "cols", "40")
        self.assertHasClass(question_element, "vLargeTextField")
        self.assertRequired(question_element)
        self.assertLabelForFieldMarkedRequired(self.question_element_id)

    # noinspection DuplicatedCode
    def test_type_field_should_be_required_select_with_empty_option_selected_by_default(self):
        self.open_add_question_page()

        type_element = self.find_element(self.type_element_locator)

        self.assertSelectTag(type_element)
        self.assertValueEmpty(type_element)
        self.assertRequired(type_element)
        self.assertLabelForFieldMarkedRequired(self.type_element_id)

        expected_options = set([("", "---------")] + Question.QuestionType.choices)
        actual_options = set(self.find_select_options(type_element))

        self.assertEqual(expected_options, actual_options)

    # noinspection DuplicatedCode
    def test_complexity_field_should_be_required_select_with_empty_option_selected_by_default(self):
        self.open_add_question_page()

        complexity_element = self.find_element(self.complexity_element_locator)

        self.assertSelectTag(complexity_element)
        self.assertValueEmpty(complexity_element)
        self.assertRequired(complexity_element)
        self.assertLabelForFieldMarkedRequired(self.complexity_element_id)

        expected_options = set([("", "---------")] + Question.Complexity.choices)
        actual_options = set(self.find_select_options(complexity_element))

        self.assertEqual(expected_options, actual_options)

    def test_number_of_points_field_should_be_required_input_number_with_empty_text_by_default(self):
        self.open_add_question_page()

        number_of_points_element = self.find_element(self.number_of_points_element_locator)

        self.assertNumberInputTag(number_of_points_element)
        self.assertTextEmpty(number_of_points_element)
        self.assertHasClass(number_of_points_element, "vIntegerField")
        self.assertRequired(number_of_points_element)
        self.assertLabelForFieldMarkedRequired(self.number_of_points_element_id)

    def test_max_attempts_to_solve_field_should_be_optional_input_number_with_empty_text_by_default(self):
        self.open_add_question_page()

        max_attempts_to_solve_element = self.find_element(self.max_attempts_to_solve_element_locator)

        self.assertNumberInputTag(max_attempts_to_solve_element)
        self.assertTextEmpty(max_attempts_to_solve_element)
        self.assertHasClass(max_attempts_to_solve_element, "vIntegerField")
        self.assertOptional(max_attempts_to_solve_element)
        self.assertLabelForFieldMarkedOptional(self.max_attempts_to_solve_element_id)

    def test_integer_correct_answer_field_should_be_optional_input_number_with_empty_text_by_default(self):
        self.open_add_question_page()

        integer_correct_answer_element = self.find_element(self.integer_correct_answer_element_locator)

        self.assertNumberInputTag(integer_correct_answer_element)
        self.assertTextEmpty(integer_correct_answer_element)

        # input isn't marked as required because this field should be validated on server based on chosen type
        self.assertOptional(integer_correct_answer_element)
        self.assertLabelForFieldMarkedRequired(self.integer_correct_answer_element_id)

    def test_decimal_correct_answer_field_should_be_optional_input_number_with_empty_text_by_default(self):
        self.open_add_question_page()

        decimal_correct_answer_element = self.find_element(self.decimal_correct_answer_element_locator)

        self.assertNumberInputTag(decimal_correct_answer_element)
        self.assertTextEmpty(decimal_correct_answer_element)

        # input isn't marked as required because this field should be validated on server based on chosen type
        self.assertOptional(decimal_correct_answer_element)
        self.assertLabelForFieldMarkedRequired(self.decimal_correct_answer_element_id)

    def test_boolean_correct_answer_field_should_be_optional_select_with_empty_option_selected_by_default(self):
        self.open_add_question_page()

        boolean_correct_answer_element = self.find_element(self.boolean_correct_answer_element_locator)

        self.assertSelectTag(boolean_correct_answer_element)
        self.assertValueEmpty(boolean_correct_answer_element)
        self.assertOptional(boolean_correct_answer_element)
        self.assertLabelForFieldMarkedRequired(self.boolean_correct_answer_element_id)

        expected_options = {("", "---------"), ("Yes", "Yes"), ("No", "No")}
        actual_options = set(self.find_select_options(boolean_correct_answer_element))

        self.assertEqual(expected_options, actual_options)

    def test_text_correct_answer_field_should_be_optional_textarea_with_empty_text_by_default(self):
        self.open_add_question_page()

        text_correct_answer_element = self.find_element(self.text_correct_answer_element_locator)

        self.assertTextareaTag(text_correct_answer_element)
        self.assertTextEmpty(text_correct_answer_element)
        self.assertAttributeEqual(text_correct_answer_element, "rows", "3")
        self.assertAttributeEqual(text_correct_answer_element, "cols", "40")
        self.assertAttributeEqual(text_correct_answer_element, "maxlength", "255")
        self.assertHasClass(text_correct_answer_element, "vLargeTextField")
        self.assertOptional(text_correct_answer_element)
        self.assertLabelForFieldMarkedRequired(self.text_correct_answer_element_id)

    # noinspection DuplicatedCode
    def test_solution_field_should_be_optional_textarea_with_empty_text_by_default(self):
        self.open_add_question_page()

        solution_element = self.find_element(self.solution_element_locator)

        self.assertTextareaTag(solution_element)
        self.assertTextEmpty(solution_element)
        self.assertAttributeEqual(solution_element, "rows", "10")
        self.assertAttributeEqual(solution_element, "cols", "40")
        self.assertHasClass(solution_element, "vLargeTextField")
        self.assertOptional(solution_element)
        self.assertLabelForFieldMarkedOptional(self.solution_element_id)

    def test_submit_with_all_empty_fields_all_required_fields_should_be_with_errors(self):
        self.open_add_question_page()
        self.submit_form()

        self.assertVisible(self.errornote_locator)
        self.assertHasRequiredValidationError(self.category_block_locator)
        self.assertHasRequiredValidationError(self.question_block_locator)
        self.assertHasRequiredValidationError(self.type_block_locator)
        self.assertHasRequiredValidationError(self.complexity_block_locator)
        self.assertHasRequiredValidationError(self.number_of_points_block_locator)

        self.assertHasNoValidationErrors(self.max_attempts_to_solve_block_locator)
        self.assertHasNoValidationErrors(self.integer_correct_answer_block_locator)
        self.assertHasNoValidationErrors(self.decimal_correct_answer_block_locator)
        self.assertHasNoValidationErrors(self.boolean_correct_answer_block_locator)
        self.assertHasNoValidationErrors(self.text_correct_answer_block_locator)
        self.assertHasNoValidationErrors(self.solution_block_locator)

    def test_number_of_points_cannot_be_less_than_1(self):
        self.open_add_question_page()
        self.set_number_of_points_value(0)
        self.submit_form()

        self.assertHasValidationErrors(self.number_of_points_block_locator,
                                       "Ensure this value is greater than or equal to 1.")

    def test_number_of_points_cannot_be_bigger_than_10(self):
        self.open_add_question_page()
        self.set_number_of_points_value(11)
        self.submit_form()

        self.assertHasValidationErrors(self.number_of_points_block_locator,
                                       "Ensure this value is less than or equal to 10.")

    def test_max_attempts_to_solve_cannot_be_less_than_1(self):
        self.open_add_question_page()
        self.set_max_attempts_to_solve_value(0)
        self.submit_form()

        self.assertHasValidationErrors(self.max_attempts_to_solve_block_locator,
                                       "Ensure this value is greater than or equal to 1.")

    def test_visibility_of_elements_based_on_selected_question_type(self):
        self.open_add_question_page()

        for question_type in ALL_QUESTION_TYPES:
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)
                self.assertVisibilityIsCorrectForType(question_type)
                self.assertNOptions(0)

    def test_multiple_changes_of_type_only_block_for_latest_type_should_be_shown(self):
        self.open_add_question_page()

        extra_type = Question.QuestionType.DECIMAL.value

        for question_type in Question.QuestionType.values + [extra_type]:
            self.set_type_value(question_type)

        # assert that after multiple changes only block for decimal type is shown
        self.assertVisibilityIsCorrectForType(extra_type)

    def test_integer_correct_answer_cannot_accept_string_value(self):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.INTEGER.value)
        self.set_integer_correct_answer_value("some value")
        self.submit_form()

        self.assertHasValidationErrors(self.integer_correct_answer_block_locator, "This field is required.")

    def test_integer_correct_answer_cannot_accept_decimal_value(self):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.INTEGER.value)
        self.set_integer_correct_answer_value(1.1)
        self.submit_form()

        self.assertHasValidationErrors(self.integer_correct_answer_block_locator, "Enter a whole number.")

    def test_form_is_filled_but_simple_correct_answer_is_empty_validation_error_should_be_shown(self):
        self.create_default_categories()
        self.open_add_question_page()

        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("2+2=?")
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)

        types_corresponding_elements = [
            self.integer_correct_answer_block_locator,
            self.decimal_correct_answer_block_locator,
            self.boolean_correct_answer_block_locator,
            self.text_correct_answer_block_locator
        ]

        for question_type, selector in zip(SIMPLE_QUESTION_TYPES, types_corresponding_elements):
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)
                self.submit_form()

                # assert that corresponding correct answer block has validation errors but other blocks don't
                self.assertHasRequiredValidationError(selector)

                for locator in types_corresponding_elements:
                    if locator != selector:
                        self.assertHasNoValidationErrors(locator)

    def test_save_integer_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_default_integer_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_save_decimal_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_default_decimal_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_save_boolean_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_default_boolean_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_save_text_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_default_text_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_open_edit_form_for_simple_question_type_should_be_prepopulated_with_saved_values(self):
        self.create_default_categories()

        integer_data = QuestionData(**{**self.default_integer_question_data._asdict(), "max_attempts_to_solve": 1,
                                       "solution": "Some solution text 1"})
        decimal_data = QuestionData(**{**self.default_decimal_question_data._asdict(), "max_attempts_to_solve": 2,
                                       "solution": "Some solution text 2"})
        boolean_data = QuestionData(**{**self.default_boolean_question_data._asdict(), "max_attempts_to_solve": 3,
                                       "solution": "Some solution text 3"})
        text_data = QuestionData(**{**self.default_text_question_data._asdict(), "max_attempts_to_solve": 4,
                                    "solution": "Some solution text 4"})
        single_choice_data = QuestionData(
            **{**self.default_single_choice_question_data._asdict(), "max_attempts_to_solve": 5,
               "solution": "Some solution text 5"})
        multiple_choice_data = QuestionData(
            **{**self.default_single_choice_question_data._asdict(), "max_attempts_to_solve": 6,
               "solution": "Some solution text 6"})
        type_to_data = {
            Question.QuestionType.INTEGER.value: integer_data,
            Question.QuestionType.DECIMAL.value: decimal_data,
            Question.QuestionType.BOOLEAN.value: boolean_data,
            Question.QuestionType.TEXT.value: text_data,
            Question.QuestionType.SINGLE_CHOICE.value: single_choice_data,
            Question.QuestionType.MULTIPLE_CHOICE.value: multiple_choice_data
        }
        func_to_data = [
            (self.create_integer_question, integer_data),
            (self.create_decimal_question, decimal_data),
            (self.create_boolean_question, boolean_data),
            (self.create_text_question, text_data),
            (self.create_single_choice_question, single_choice_data),
            (self.create_multiple_choice_question, multiple_choice_data)
        ]

        for create_question_func, question_data in func_to_data:
            create_question_func(question_data)

        for change_link in self.get_change_links_for_questions():
            self.open_page(change_link)

            question_type = self.get_type_value()

            with self.subTest(question_type=question_type):
                expected_data = type_to_data[question_type]

                category_name = self.get_category_name()
                question = self.get_question_value()
                complexity = self.get_complexity_value()
                number_of_points = self.get_number_of_points_value()
                max_attempts_to_solve = self.get_max_attempts_to_solve_value()
                correct_answer = self.get_correct_answer_value()
                solution = self.get_solution_value()
                options = self.get_question_options()

                expected_correct_answer = str(
                    expected_data.correct_answer) if expected_data.correct_answer is not None else None

                self.assertEqual(expected_data.category_name, category_name)
                self.assertEqual(expected_data.question, question)
                self.assertEqual(expected_data.complexity, complexity)
                self.assertEqual(str(expected_data.number_of_points), number_of_points)
                self.assertEqual(str(expected_data.max_attempts_to_solve), max_attempts_to_solve)
                self.assertEqual(expected_correct_answer, correct_answer)
                self.assertEqual(expected_data.solution, solution)
                self.assertEqual(expected_data.options or [], options)
                self.assertVisibilityIsCorrectForType(question_type)

    def test_form_is_filled_with_options_dependent_type_correct_answer_inputs_should_not_be_invalid(self):
        self.create_default_categories()
        self.open_add_question_page()

        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("2+2=?")
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)

        for question_type in COMPLEX_QUESTION_TYPES:
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)
                self.submit_form()

                self.assertHasNoValidationErrors(self.integer_correct_answer_block_locator)
                self.assertHasNoValidationErrors(self.decimal_correct_answer_block_locator)
                self.assertHasNoValidationErrors(self.boolean_correct_answer_block_locator)
                self.assertHasNoValidationErrors(self.text_correct_answer_block_locator)

    def test_form_is_filled_with_options_dependent_type_no_options_added_validation_error_should_be_shown(self):
        self.create_default_categories()
        self.open_add_question_page()

        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("2+2=?")
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)

        for question_type in COMPLEX_QUESTION_TYPES:
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)
                self.submit_form()

                self.assertHasValidationErrors(self.options_locator, error_class=None,
                                               error_message="At least two options should be specified.")

    def test_form_is_filled_with_options_dependent_type_options_empty_validation_error_should_be_shown(self):
        self.create_default_categories()

        for question_type in COMPLEX_QUESTION_TYPES:
            with self.subTest(question_type=question_type):
                self.open_add_question_page()
                self.set_category_value_by_name("Elementary Algebra")
                self.set_question_value("2+2=?")
                self.set_type_value(question_type)
                self.set_complexity_value(Question.Complexity.EASY.value)
                self.set_number_of_points_value(1)

                self.create_option()
                self.create_option("5")
                self.create_option()
                self.submit_form()

                self.assertHasRequiredValidationError("#options-0 .field-value", error_class=None)
                self.assertHasNoValidationErrors("#options-1 .field-value")
                self.assertHasRequiredValidationError("#options-2 .field-value", error_class=None)

    def test_form_is_filled_with_options_dependent_type_options_have_duplicates_validation_error_should_be_shown(self):
        self.create_default_categories()

        for question_type in COMPLEX_QUESTION_TYPES:
            with self.subTest(question_type=question_type):
                self.open_add_question_page()
                self.set_category_value_by_name("Elementary Algebra")
                self.set_question_value("2+2=?")
                self.set_type_value(question_type)
                self.set_complexity_value(Question.Complexity.EASY.value)
                self.set_number_of_points_value(1)

                self.create_option("5")
                self.create_option("5")
                self.submit_form()

                self.assertHasValidationErrors(self.options_locator, error_class=None,
                                               error_message="Some options have the same values.")

    def test_form_is_filled_with_options_dependent_type_no_correct_option_chosen_validation_error_should_be_shown(self):
        self.create_default_categories()

        errors_for_type = {
            Question.QuestionType.SINGLE_CHOICE.value:
                "For single choice question type you need to specify exactly one correct option.",
            Question.QuestionType.MULTIPLE_CHOICE.value:
                "For multiple choice question type you need to specify at least one correct option."
        }

        for question_type in COMPLEX_QUESTION_TYPES:
            with self.subTest(question_type=question_type):
                self.open_add_question_page()
                self.set_category_value_by_name("Elementary Algebra")
                self.set_question_value("2+2=?")
                self.set_type_value(question_type)
                self.set_complexity_value(Question.Complexity.EASY.value)
                self.set_number_of_points_value(1)

                self.create_option("3")
                self.create_option("4")
                self.create_option("5")
                self.submit_form()

                self.assertHasValidationErrors(self.options_locator, error_class=None,
                                               error_message=errors_for_type[question_type])

    def test_single_choice_question_correct_option_chosen_should_be_saved_properly(self):
        self.create_default_categories()
        self.open_add_question_page()
        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("2+2=?")
        self.set_type_value(Question.QuestionType.SINGLE_CHOICE.value)
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)

        self.create_option("3")
        self.create_option("4", True)
        self.create_option("5")
        self.submit_form()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_multiple_choice_question_correct_options_chosen_should_be_saved_properly(self):
        self.create_default_categories()
        self.open_add_question_page()
        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("Choose all correct options.")
        self.set_type_value(Question.QuestionType.MULTIPLE_CHOICE.value)
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)

        self.create_option("2+2=4", True)
        self.create_option("2-3=5", False)
        self.create_option("3*9=27", True)
        self.create_option("12/12=1", True)
        self.submit_form()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def assertVisibilityIsCorrectForType(self, question_type):
        for visible_element in self.elements_visibility_by_type[question_type].visible_elements:
            self.assertVisible(visible_element)

        for invisible_element in self.elements_visibility_by_type[question_type].invisible_elements:
            self.assertInvisible(invisible_element)

    def assertNOptions(self, number_of_options):
        self.assertEqual(number_of_options, len(self.get_question_options()))

    def assertCurrentPageIsQuestionsList(self):
        self.assertEqual(self.getQuestionListPage(), self.selenium.current_url)

    def getQuestionListPage(self):
        return f"{self.live_server_url}/admin/problems/question/"

    def assertQuestionsListHasNElements(self, expected_number_of_questions):
        question_rows = self.get_questions_rows()
        actual_number_of_questions = len(question_rows)

        self.assertEqual(expected_number_of_questions, actual_number_of_questions)

    def get_change_links_for_questions(self):
        return [link.get_attribute("href")
                for row in self.get_questions_rows()
                for link in row.find_elements_by_css_selector(".field-category > a")]

    def get_questions_rows(self):
        return self.selenium.find_elements_by_css_selector("#result_list tbody tr")

    def create_default_categories(self):
        for name in self.default_categories:
            Category.objects.create(name=name)

    def find_category_select(self):
        category_element = self.selenium.find_element_by_id("id_category")
        category_select = ui.Select(category_element)

        return category_select

    def open_add_question_page(self):
        self.open_page("/admin/problems/question/add/")

    def set_category_value_by_name(self, name):
        category_select = self.find_category_select()
        category_select.select_by_visible_text(name)

    def get_category_name(self):
        category_select = self.find_category_select()
        category_name = category_select.first_selected_option.get_attribute("innerText")

        return category_name

    def set_question_value(self, value):
        question_element = self.find_element(self.question_element_locator)
        question_element.send_keys(str(value))

    def get_question_value(self):
        question_element = self.find_element(self.question_element_locator)
        question_value = question_element.get_attribute("value")

        return question_value

    def set_type_value(self, value):
        type_element = self.find_element(self.type_element_locator)
        type_select = ui.Select(type_element)
        type_select.select_by_value(str(value))

    def get_type_value(self):
        type_element = self.find_element(self.type_element_locator)
        type_value = type_element.get_attribute("value")

        return type_value

    def set_complexity_value(self, value):
        complexity_element = self.find_element(self.complexity_element_locator)
        complexity_element.send_keys(str(value))

    def get_complexity_value(self):
        complexity_element = self.find_element(self.complexity_element_locator)
        complexity_value = complexity_element.get_attribute("value")

        return complexity_value

    def set_number_of_points_value(self, value):
        number_of_points_element = self.find_element(self.number_of_points_element_locator)
        number_of_points_element.send_keys(str(value))

    def get_number_of_points_value(self):
        number_of_points_element = self.find_element(self.number_of_points_element_locator)
        number_of_points_value = number_of_points_element.get_attribute("value")

        return number_of_points_value

    def set_max_attempts_to_solve_value(self, value):
        max_attempts_to_solve_element = self.find_element(self.max_attempts_to_solve_element_locator)
        max_attempts_to_solve_element.send_keys(str(value))

    def get_max_attempts_to_solve_value(self):
        max_attempts_to_solve_element = self.find_element(self.max_attempts_to_solve_element_locator)
        max_attempts_to_solve_value = max_attempts_to_solve_element.get_attribute("value")

        return max_attempts_to_solve_value

    def set_integer_correct_answer_value(self, value):
        integer_correct_answer_element = self.find_element(self.integer_correct_answer_element_locator)
        integer_correct_answer_element.send_keys(str(value))

    def set_decimal_correct_answer_value(self, value):
        decimal_correct_answer_element = self.find_element(self.decimal_correct_answer_element_locator)
        decimal_correct_answer_element.send_keys(str(value))

    def set_boolean_correct_answer_value(self, value):
        boolean_correct_answer_element = self.find_element(self.boolean_correct_answer_element_locator)
        boolean_correct_answer_select = ui.Select(boolean_correct_answer_element)
        boolean_correct_answer_select.select_by_value(str(value))

    def set_text_correct_answer_value(self, value):
        text_correct_answer_element = self.find_element(self.text_correct_answer_element_locator)
        text_correct_answer_element.send_keys(str(value))

    def get_correct_answer_value(self):
        element = None
        type_value = self.get_type_value()

        if type_value == Question.QuestionType.INTEGER.value:
            element = self.find_element(self.integer_correct_answer_element_locator)
        elif type_value == Question.QuestionType.DECIMAL.value:
            element = self.find_element(self.decimal_correct_answer_element_locator)
        if type_value == Question.QuestionType.BOOLEAN.value:
            element = self.find_element(self.boolean_correct_answer_element_locator)
        elif type_value == Question.QuestionType.TEXT.value:
            element = self.find_element(self.text_correct_answer_element_locator)

        if element:
            return element.get_attribute("value")
        else:
            return None

    def set_solution_value(self, value):
        solution_element = self.find_element(self.solution_element_locator)
        solution_element.send_keys(str(value))

    def get_solution_value(self):
        solution_element = self.find_element(self.solution_element_locator)
        solution_value = solution_element.get_attribute("value")

        return solution_value

    def get_question_options(self):
        options_rows = self.find_element(self.options_locator).find_elements_by_css_selector(
            "fieldset.module table tbody tr:not(.add-row, .empty-form)")
        options = []

        for row in options_rows:
            value = row.find_element_by_css_selector(".field-value input").get_attribute("value")
            checked = row.find_element_by_css_selector(".field-is_correct input").get_property("checked")

            options.append(OptionData(value, checked))

        return options

    def create_default_integer_question(self):
        self.create_integer_question(self.default_integer_question_data)

    def create_integer_question(self, data: QuestionData):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.INTEGER.value)
        self.set_integer_correct_answer_value(data.correct_answer)
        self.fill_question_common_fields(data)
        self.submit_form()

    def create_default_decimal_question(self):
        self.create_decimal_question(self.default_decimal_question_data)

    def create_decimal_question(self, data: QuestionData):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.DECIMAL.value)
        self.set_decimal_correct_answer_value(data.correct_answer)
        self.fill_question_common_fields(data)
        self.submit_form()

    def create_default_boolean_question(self):
        self.create_boolean_question(self.default_boolean_question_data)

    def create_boolean_question(self, data: QuestionData):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.BOOLEAN.value)
        self.set_boolean_correct_answer_value(data.correct_answer)
        self.fill_question_common_fields(data)
        self.submit_form()

    def create_default_text_question(self):
        self.create_text_question(self.default_text_question_data)

    def create_text_question(self, data: QuestionData):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.TEXT.value)
        self.set_text_correct_answer_value(data.correct_answer)
        self.fill_question_common_fields(data)
        self.submit_form()

    def create_default_single_choice_question(self):
        self.create_single_choice_question(self.default_single_choice_question_data)

    def create_single_choice_question(self, data: QuestionData):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.SINGLE_CHOICE.value)
        self.fill_question_common_fields(data)
        self.fill_options(data.options)
        self.submit_form()

    def create_default_multiple_choice_question(self):
        self.create_multiple_choice_question(self.default_multiple_choice_question_data)

    def create_multiple_choice_question(self, data: QuestionData):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.MULTIPLE_CHOICE.value)
        self.fill_question_common_fields(data)
        self.fill_options(data.options)
        self.submit_form()

    def fill_question_common_fields(self, data: QuestionData):
        self.set_category_value_by_name(data.category_name)
        self.set_question_value(data.question)
        self.set_complexity_value(data.complexity)
        self.set_number_of_points_value(data.number_of_points)
        self.set_max_attempts_to_solve_value(data.max_attempts_to_solve)
        self.set_solution_value(data.solution)

    def fill_options(self, options: List[OptionData]):
        for option in options:
            self.create_option(option.value, option.correct)

    def create_option(self, value=None, correct=False):
        question_type = self.get_type_value()
        is_correct_input_type = "radio" if question_type == Question.QuestionType.SINGLE_CHOICE.value else "checkbox"

        add_option_link = self.find_element(self.add_new_option_locator)
        add_option_link.click()

        new_option_row = self.find_element(self.new_option_row_locator)

        if value is not None:
            new_option_row_value_element = new_option_row.find_element_by_css_selector(".field-value input")
            new_option_row_value_element.send_keys(str(value))

        if correct:
            new_option_row_correct_element = new_option_row.find_element_by_css_selector(
                f".field-is_correct input[type={is_correct_input_type}]")
            new_option_row_correct_element.click()

    def submit_form(self):
        save_button = self.find_element(self.save_button_locator)
        save_button.click()
