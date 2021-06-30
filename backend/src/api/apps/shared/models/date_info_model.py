from django.db import models
from django.utils.translation import gettext_lazy as _


class ChangeDateInfoModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, null=False, verbose_name=_("Created"))
    changed = models.DateTimeField(auto_now=True, null=False, verbose_name=_("Changed"))

    class Meta:
        abstract = True
