from django.contrib import admin
from app_manage.models import Project,Module


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'status', 'create_time']  #显示字段

class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'create_time', 'project']  #显示字段




admin.site.register(Project, ProjectAdmin)
admin.site.register(Module, ModuleAdmin)