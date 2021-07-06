from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.apps.problems.models import Category
from api.apps.shared.models import ChangeDateInfoModel


class Question(ChangeDateInfoModel):
    class QuestionType(models.TextChoices):
        INTEGER = "Integer", _("Integer")
        DECIMAL = "Decimal", _("Decimal")
        TEXT = "Text", _("Text")
        BOOLEAN = "Boolean", _("Boolean")
        SINGLE_CHOICE = "Single Choice", _("Single Choice")
        MULTIPLE_CHOICE = "Multiple Choice", _("Multiple Choice")

    class Complexity(models.TextChoices):
        EASY = "Easy", _("Easy")
        MEDIUM = "Medium", _("Medium")
        HARD = "Hard", _("Hard")
        EXTREMELY_HARD = "Extremely Hard", _("Extremely Hard")

    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, related_name="questions",
                                 verbose_name=_("Category"))
    text = models.TextField(max_length=2048, verbose_name=_("Question"))
    type = models.CharField(max_length=32, verbose_name=_("Type"), choices=QuestionType.choices)
    complexity = models.CharField(max_length=32, verbose_name=_("Complexity"), choices=Complexity.choices)
    number_of_points = models.IntegerField(verbose_name=_("Number of Points"), validators=[
        MinValueValidator(1), MaxValueValidator(10)
    ])
    max_attempts_to_solve = models.IntegerField(
        null=True, blank=True,
        verbose_name=_("Max Attempts To Solve"),
        validators=[
            MinValueValidator(1)
        ]
    )
    correct_answer = models.CharField(max_length=255, null=True, verbose_name=_("Correct Answer"))
    solution = models.TextField(null=True, blank=True, verbose_name=_("Solution"))

    def __str__(self):
        return self.text

    class Meta:
        db_table = "problems_questions"
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        constraints = [models.CheckConstraint(
            check=models.Q(number_of_points__gte=1) & models.Q(number_of_points__lte=10),
            name="Number of Points is an integer value between 1 and 10"
        ), models.CheckConstraint(
            check=models.Q(max_attempts_to_solve__gte=1),
            name="Max Attempts To Solve is a positive integer value"
        )]
        indexes = [
            models.Index(fields=["type"]),
            models.Index(fields=["complexity"])
        ]
