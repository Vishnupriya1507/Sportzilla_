from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Question, CustomUser

# Register your models here.
admin.site.register(Question)
admin.site.register(CustomUser)

