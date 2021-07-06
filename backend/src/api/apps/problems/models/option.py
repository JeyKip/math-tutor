from django.db import models
from django.utils.translation import gettext_lazy as _

from api.apps.problems.models import Question
from api.apps.shared.models import ChangeDateInfoModel


class Option(ChangeDateInfoModel):
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name="options",
                                 verbose_name=_("Question"))
    value = models.CharField(max_length=2048, verbose_name=_("Value"))
    is_correct = models.BooleanField(verbose_name=_("Is Correct"))

    def __str__(self):
        return self.value

    class Meta:
        db_table = "problems_questions_options"
        verbose_name = _("Option")
        verbose_name_plural = _("Options")
        constraints = [
            models.UniqueConstraint(fields=("question", "value"), name="question_value_unique_constraint")
        ]
