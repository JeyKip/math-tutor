from api.apps.problems.models import Question

SIMPLE_QUESTION_TYPES = [
    Question.QuestionType.INTEGER.value,
    Question.QuestionType.DECIMAL.value,
    Question.QuestionType.BOOLEAN.value,
    Question.QuestionType.TEXT.value,
]

COMPLEX_QUESTION_TYPES = [
    Question.QuestionType.SINGLE_CHOICE.value,
    Question.QuestionType.MULTIPLE_CHOICE.value,
]

ALL_QUESTION_TYPES = SIMPLE_QUESTION_TYPES + COMPLEX_QUESTION_TYPES
