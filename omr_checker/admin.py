from django.contrib import admin

# Register your models here.
from omr_checker import models

admin.site.register(models.Class)
admin.site.register(models.Student)
admin.site.register(models.Exam)
admin.site.register(models.OMRUpload)
