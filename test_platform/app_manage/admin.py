from django.contrib import admin
from app_manage.models import Project


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'status', 'create_time']  #显示字段


admin.site.register(Project, ProjectAdmin)