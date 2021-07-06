from django.db import models
from django.utils.translation import gettext_lazy as _

from api.apps.shared.models import ChangeDateInfoModel


class Category(ChangeDateInfoModel):
    name = models.CharField(max_length=128, unique=True, verbose_name=_("Name"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created"]
        db_table = "problems_categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
