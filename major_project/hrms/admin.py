from django.contrib import admin
from hrms.models import Event
from .models import Event,Employee,Department,Kin,Recruitment,JobPost,Performance,Task,TrainingProgram
# Register your models here.
admin.site.register([Event,Employee,Department,Kin,Recruitment,JobPost,Performance,Task,TrainingProgram])


