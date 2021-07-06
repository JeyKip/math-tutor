from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import Field
from django.forms.formsets import DELETION_FIELD_NAME
from django.utils.translation import gettext_lazy as _

from api.apps.problems.models import Question, Option


def validate_boolean_value(value):
    return value in ["Yes", "No"]


QUESTION_TYPES_TO_SAVE_CORRECT_ANSWER = [
    Question.QuestionType.INTEGER.value.lower(),
    Question.QuestionType.DECIMAL.value.lower(),
    Question.QuestionType.BOOLEAN.value.lower(),
    Question.QuestionType.TEXT.value.lower(),
]


class AdminOptionInlineFormset(forms.BaseInlineFormSet):
    options_error_messages = {
        "incorrect_number_of_valid_options": _("At least two options should be specified."),
        "options_have_duplicates": _("Some options have the same values."),
        "incorrect_number_of_single_choice_options": _(
            "For single choice question type you need to specify exactly one correct option."),
        "incorrect_number_of_multiple_choice_options": _(
            "For multiple choice question type you need to specify at least one correct option."
        )
    }

    def clean(self):
        if not self.__options_should_be_specified():
            return

        number_of_valid_options, number_of_correct_options, number_of_distinct_options = self.__validate_options()

        if not self.is_valid():
            return

        if number_of_valid_options < 2:
            raise ValidationError(self.options_error_messages["incorrect_number_of_valid_options"])

        if number_of_distinct_options != number_of_valid_options:
            raise ValidationError(self.options_error_messages["options_have_duplicates"])

        if self.__single_choice and number_of_correct_options != 1:
            raise ValidationError(self.options_error_messages["incorrect_number_of_single_choice_options"])

        if self.__multiple_choice and number_of_correct_options == 0:
            raise ValidationError(self.options_error_messages["incorrect_number_of_multiple_choice_options"])

    def __options_should_be_specified(self):
        return self.__question_type in [
            Question.QuestionType.SINGLE_CHOICE.value,
            Question.QuestionType.MULTIPLE_CHOICE.value
        ]

    @property
    def __question_type(self):
        return self.data["type"] if "type" in self.data else None

    def __validate_options(self):
        number_of_valid_options = 0
        number_of_correct_options = 0
        distinct_options = set()

        for form in self.forms:
            if not form.is_valid() or form in self.deleted_forms:
                continue

            value, is_correct = form.cleaned_data.get("value"), form.cleaned_data.get("is_correct", False)

            if not value:
                form.errors["value"] = self.error_class([Field.default_error_messages["required"]])
                continue

            number_of_valid_options += 1

            if is_correct:
                number_of_correct_options += 1

            distinct_options.add(value)

        return number_of_valid_options, number_of_correct_options, len(distinct_options)

    @property
    def __single_choice(self):
        return self.__question_type == Question.QuestionType.SINGLE_CHOICE

    @property
    def __multiple_choice(self):
        return self.__question_type == Question.QuestionType.MULTIPLE_CHOICE

    def save(self, commit=True):
        if not self.__options_should_be_specified():
            self.__mark_options_to_delete()

        super(AdminOptionInlineFormset, self).save(commit)

    def __mark_options_to_delete(self):
        for form in self.forms:
            form.cleaned_data[DELETION_FIELD_NAME] = True


class AdminOptionInline(admin.TabularInline):
    model = Option
    formset = AdminOptionInlineFormset
    extra = 0


class AdminQuestionChangeForm(forms.ModelForm):
    validators = {
        Question.QuestionType.BOOLEAN.value.lower(): validate_boolean_value
    }
    integer_correct_answer = forms.IntegerField(label=_("Correct Answer"), required=False)
    decimal_correct_answer = forms.DecimalField(label=_("Correct Answer"), required=False)
    boolean_correct_answer = forms.ChoiceField(
        label=_("Correct Answer"),
        required=False,
        choices=((None, "-==-"), ("Yes", _("Yes")), ("No", _("No")))
    )

    text_correct_answer = forms.CharField(
        label=_("Correct Answer"),
        max_length=255,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "cols": 40, "class": "vLargeTextField"})
    )

    def clean_integer_correct_answer(self):
        return self.__validate_correct_answer(Question.QuestionType.INTEGER.value)

    def clean_decimal_correct_answer(self):
        return self.__validate_correct_answer(Question.QuestionType.DECIMAL.value)

    def clean_boolean_correct_answer(self):
        return self.__validate_correct_answer(Question.QuestionType.BOOLEAN.value)

    def clean_text_correct_answer(self):
        return self.__validate_correct_answer(Question.QuestionType.TEXT.value)

    def __validate_correct_answer(self, required_type):
        required_field_type = required_type.lower()
        required_field = f"{required_field_type}_correct_answer"

        question_type = self.__get_question_type()
        correct_answer = self.cleaned_data[required_field]

        if question_type == required_field_type:
            if self.__correct_answer_is_empty(correct_answer):
                raise ValidationError(Field.default_error_messages["required"])

            if question_type in self.validators:
                if not self.validators[question_type](correct_answer):
                    raise ValidationError(_('Value of the field is invalid.'))

        return correct_answer

    def __correct_answer_is_empty(self, value):
        if value in Field.empty_values:
            return True

        if isinstance(value, str) and value.strip() in Field.empty_values:
            return True

        return False

    def save(self, commit=True):
        model = super().save(commit)
        model.correct_answer = self.__get_correct_answer()

        return model

    def __get_correct_answer(self):
        question_type = self.__get_question_type()

        if question_type in QUESTION_TYPES_TO_SAVE_CORRECT_ANSWER:
            return self.cleaned_data[f"{question_type}_correct_answer"]

    def __get_question_type(self):
        return self.cleaned_data["type"].lower()

    class Meta:
        model = Question
        fields = [
            "category",
            "text",
            "type",
            "complexity",
            "number_of_points",
            "max_attempts_to_solve",
            "integer_correct_answer",
            "decimal_correct_answer",
            "boolean_correct_answer",
            "text_correct_answer",
            "solution"
        ]


@admin.register(Question)
class AdminQuestion(admin.ModelAdmin):
    form = AdminQuestionChangeForm
    list_display = ("category", "type", "complexity", "text")
    list_filter = ("category",)
    list_per_page = 50
    search_fields = ("category", "type", "complexity")
    sortable_by = ("-created",)
    inlines = [AdminOptionInline]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(AdminQuestion, self).get_form(request, obj, change, **kwargs)
        self.__initialize_correct_answer_fields(form, obj)
        return form

    def __initialize_correct_answer_fields(self, form, obj):
        if not obj:
            return

        obj_type = obj.type.lower()

        for question_type in QUESTION_TYPES_TO_SAVE_CORRECT_ANSWER:
            field_name = f"{question_type}_correct_answer"
            value = obj.correct_answer if obj_type == question_type else None

            form.base_fields[field_name].initial = value
