from django.contrib.auth.models import Group
from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.ArmyPerson)
class ArmyPersonModel(admin.ModelAdmin):
    search_fields = ("code", "name")
    search_help_text = "ابحث عن كود...."
    list_display = ("code", "name", "branch", "rank")

admin.site.register(models.Branch)
admin.site.register(models.Rank)
admin.site.unregister(Group)
