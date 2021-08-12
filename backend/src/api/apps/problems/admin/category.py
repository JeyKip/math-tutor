from django.contrib import admin

from api.apps.problems.models import Category


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ("name", "created", "changed")
    search_fields = ("name",)
    sortable_by = ("name", "created")
