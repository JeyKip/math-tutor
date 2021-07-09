from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui

from api.apps.problems.models import Category, Question
from .admin_e2e_base_test_case import AdminE2EBaseTestCase


class QuestionEditTestCase(AdminE2EBaseTestCase):
    simple_types = [
        Question.QuestionType.INTEGER.value,
        Question.QuestionType.DECIMAL.value,
        Question.QuestionType.BOOLEAN.value,
        Question.QuestionType.TEXT.value
    ]
    complex_types = [
        Question.QuestionType.SINGLE_CHOICE.value,
        Question.QuestionType.MULTIPLE_CHOICE.value
    ]
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
        actual_options = set(self.find_options(type_element))

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
        actual_options = set(self.find_options(complexity_element))

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
        actual_options = set(self.find_options(boolean_correct_answer_element))

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

    def test_integer_type_selected_integer_correct_answer_should_be_shown(self):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.INTEGER.value)

        self.assertVisible(self.integer_correct_answer_block_locator)
        self.assertInvisible(self.decimal_correct_answer_block_locator)
        self.assertInvisible(self.boolean_correct_answer_block_locator)
        self.assertInvisible(self.text_correct_answer_block_locator)
        self.assertInvisible(self.options_locator)

    def test_decimal_type_selected_decimal_correct_answer_should_be_shown(self):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.DECIMAL.value)

        self.assertInvisible(self.integer_correct_answer_block_locator)
        self.assertVisible(self.decimal_correct_answer_block_locator)
        self.assertInvisible(self.boolean_correct_answer_block_locator)
        self.assertInvisible(self.text_correct_answer_block_locator)
        self.assertInvisible(self.options_locator)

    def test_boolean_type_selected_boolean_correct_answer_should_be_shown(self):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.BOOLEAN.value)

        self.assertInvisible(self.integer_correct_answer_block_locator)
        self.assertInvisible(self.decimal_correct_answer_block_locator)
        self.assertVisible(self.boolean_correct_answer_block_locator)
        self.assertInvisible(self.text_correct_answer_block_locator)
        self.assertInvisible(self.options_locator)

    def test_text_type_selected_text_correct_answer_should_be_shown(self):
        self.open_add_question_page()
        self.set_type_value(Question.QuestionType.TEXT.value)

        self.assertInvisible(self.integer_correct_answer_block_locator)
        self.assertInvisible(self.decimal_correct_answer_block_locator)
        self.assertInvisible(self.boolean_correct_answer_block_locator)
        self.assertVisible(self.text_correct_answer_block_locator)
        self.assertInvisible(self.options_locator)

    def test_choice_type_selected_options_editor_with_empty_list_should_be_shown(self):
        self.open_add_question_page()

        for question_type in [Question.QuestionType.SINGLE_CHOICE.value, Question.QuestionType.MULTIPLE_CHOICE.value]:
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)

                self.assertInvisible(self.integer_correct_answer_block_locator)
                self.assertInvisible(self.decimal_correct_answer_block_locator)
                self.assertInvisible(self.boolean_correct_answer_block_locator)
                self.assertInvisible(self.text_correct_answer_block_locator)
                self.assertVisible(self.options_locator)
                self.assertNOptions(0)

    def test_multiple_changes_of_type_only_block_for_latest_type_should_be_shown(self):
        self.open_add_question_page()

        for question_type in Question.QuestionType.values + [Question.QuestionType.DECIMAL.value]:
            self.set_type_value(question_type)

        # assert that after multiple changes only block for decimal type is shown
        self.assertInvisible(self.integer_correct_answer_block_locator)
        self.assertVisible(self.decimal_correct_answer_block_locator)
        self.assertInvisible(self.boolean_correct_answer_block_locator)
        self.assertInvisible(self.text_correct_answer_block_locator)
        self.assertInvisible(self.options_locator)

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

        types_to_check = self.simple_types
        types_corresponding_elements = [
            self.integer_correct_answer_block_locator,
            self.decimal_correct_answer_block_locator,
            self.boolean_correct_answer_block_locator,
            self.text_correct_answer_block_locator
        ]

        for question_type, selector in zip(types_to_check, types_corresponding_elements):
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)
                self.submit_form()

                # assert that corresponding correct answer block has validation errors but other blocks don't
                self.assertHasRequiredValidationError(selector)

                for locator in types_corresponding_elements:
                    if locator != selector:
                        self.assertHasNoValidationErrors(locator)

    def test_form_is_filled_with_options_dependent_type_no_options_added_validation_error_should_be_shown(self):
        self.create_default_categories()
        self.open_add_question_page()

        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("2+2=?")
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)

        for question_type in self.complex_types:
            with self.subTest(question_type=question_type):
                self.set_type_value(question_type)
                self.submit_form()

                self.assertHasValidationErrors(self.options_locator, error_class=None,
                                               error_message="At least two options should be specified.")
                self.assertHasNoValidationErrors(self.integer_correct_answer_block_locator)
                self.assertHasNoValidationErrors(self.decimal_correct_answer_block_locator)
                self.assertHasNoValidationErrors(self.boolean_correct_answer_block_locator)
                self.assertHasNoValidationErrors(self.text_correct_answer_block_locator)

    def test_save_integer_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_integer_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_open_integer_type_for_edit_form_should_be_prepopulated_with_saved_values(self):
        # fulfill all fields here
        pass

    def test_save_decimal_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_decimal_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_save_boolean_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_boolean_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def test_save_text_type_question_with_required_fields_only_form_should_be_properly_saved(self):
        self.create_default_categories()
        self.create_text_question()

        self.assertCurrentPageIsQuestionsList()
        self.assertQuestionsListHasNElements(1)

    def assertNOptions(self, number_of_options):
        options = self.find_element(self.options_locator).find_elements_by_css_selector(
            "fieldset.module table tbody tr:not(.add-row, .empty-form)")

        self.assertEqual(number_of_options, len(options))

    def assertCurrentPageIsQuestionsList(self):
        self.assertEqual(self.getQuestionListPage(), self.selenium.current_url)

    def getQuestionListPage(self):
        return f"{self.live_server_url}/admin/problems/question/"

    def assertQuestionsListHasNElements(self, expected_number_of_questions):
        question_rows = self.selenium.find_elements_by_css_selector("#result_list tbody tr")
        actual_number_of_questions = len(question_rows)

        self.assertEqual(expected_number_of_questions, actual_number_of_questions)

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

    def set_question_value(self, value):
        question_element = self.find_element(self.question_element_locator)
        question_element.send_keys(str(value))

    def set_type_value(self, value):
        type_element = self.find_element(self.type_element_locator)
        type_select = ui.Select(type_element)
        type_select.select_by_value(str(value))

    def set_complexity_value(self, value):
        complexity_element = self.find_element(self.complexity_element_locator)
        complexity_element.send_keys(str(value))

    def set_max_attempts_to_solve_value(self, value):
        max_attempts_to_solve_element = self.find_element(self.max_attempts_to_solve_element_locator)
        max_attempts_to_solve_element.send_keys(str(value))

    def set_number_of_points_value(self, value):
        number_of_points_element = self.find_element(self.number_of_points_element_locator)
        number_of_points_element.send_keys(str(value))

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

    def create_integer_question(self):
        self.open_add_question_page()
        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("2+2=?")
        self.set_type_value(Question.QuestionType.INTEGER.value)
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)
        self.set_integer_correct_answer_value(4)
        self.submit_form()

    def create_decimal_question(self):
        self.open_add_question_page()
        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("9 / 2 = ?")
        self.set_type_value(Question.QuestionType.DECIMAL.value)
        self.set_complexity_value(Question.Complexity.EASY.value)
        self.set_number_of_points_value(1)
        self.set_decimal_correct_answer_value(4.5)
        self.submit_form()

    def create_boolean_question(self):
        self.open_add_question_page()
        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("The logarithm is the inverse function to exponentiation.")
        self.set_type_value(Question.QuestionType.BOOLEAN.value)
        self.set_complexity_value(Question.Complexity.MEDIUM.value)
        self.set_number_of_points_value(2)
        self.set_boolean_correct_answer_value("Yes")
        self.submit_form()

    def create_text_question(self):
        self.open_add_question_page()
        self.set_category_value_by_name("Elementary Algebra")
        self.set_question_value("What is the inverse function to exponentiation?")
        self.set_type_value(Question.QuestionType.TEXT.value)
        self.set_complexity_value(Question.Complexity.MEDIUM.value)
        self.set_number_of_points_value(2)
        self.set_text_correct_answer_value("Logarithm")
        self.submit_form()

    def submit_form(self):
        save_button = self.find_element(self.save_button_locator)
        save_button.click()
