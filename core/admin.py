from django.contrib import admin
from .models import Project, Column, Task, CheckList, ProjectInvite

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id','slug','owner','title','description','archived', 'favourite', 'is_active', 'created_at', 'updated_at')
    list_filter = ('archived', 'owner', 'favourite', 'is_active', 'created_at', 'updated_at')
    search_fields =  ('name',)
    
@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('id','slug','title', 'project', 'created_at', 'updated_at')
    list_filter = ( 'created_at', 'updated_at')
    search_fields =  ('title',)
    
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','slug','title','description','column', 'priority', 'due_date', 'created_at', 'updated_at')
    list_filter = ( 'column', 'priority', 'due_date', 'created_at', 'updated_at')
    search_fields =  ('title',)
    
@admin.register(CheckList)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'task', 'checked', 'created_at', 'updated_at')
    list_filter = ( 'task', 'checked','created_at', 'updated_at')
    search_fields =  ('title',)
    
@admin.register(ProjectInvite)
class ProjectInviteAdmin(admin.ModelAdmin):
    list_display = ('id', 'invited_user', 'project', 'created_at', 'updated_at')
    list_filter = ('invited_user','created_at', 'updated_at')
    search_fields =  ('invited_user__email',)
    