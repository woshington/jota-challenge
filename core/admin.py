from django.contrib import admin

# Register your models here.

from core.models import Vertical, Plan

admin.site.register(Vertical)
admin.site.register(Plan)