from django.urls import path
from .views import(
    create_project, get_user_projects, get_invited_projects, update_project, get_project, delete_project, 
    add_column, get_project_columns,delete_column,add_task, 
    get_tasks, update_task, get_task, add_checklist, get_checklists,
    update_checklist, delete_checklist,
    search_users, invite_member, get_invites, update_invite_status)
urlpatterns = [
    path('core/create_project/', create_project, name='create_project'),
    path('core/get_user_projects/', get_user_projects, name='get_user_projects'),
    path('core/get_invited_projects/', get_invited_projects, name='get_invited_projects'),
    path('core/update_project/', update_project, name='update_project'),
    path('core/get_project/<int:project_id>/', get_project, name='get_project'),
    path('core/delete_project/<int:project_id>/', delete_project, name='delete_project'),
    path('core/add_column/<int:project_id>/', add_column, name='add_column'),
    path('core/get_project_columns/<int:project_id>/', get_project_columns, name='get_project_columns'),
    path('core/delete_column/<int:column_id>/', delete_column, name='delete_column'),
    path('core/add_task/<int:column_id>/', add_task, name='add_task'),
    path('core/get_tasks/<int:column_id>/', get_tasks, name='get_tasks'),
    path('core/get_task/<int:task_id>/', get_task, name='get_task'),
    path('core/update_task/<int:task_id>/', update_task, name='update_task'),
    path('core/add_checklist/<int:task_id>/', add_checklist, name='add_checklist'),
    path('core/get_checklists/<int:task_id>/', get_checklists, name='get_checklists'),
    path('core/update_checklist/<int:checklist_id>/', update_checklist, name='update_checklist'),
    path('core/delete_checklist/<int:checklist_id>/', delete_checklist, name='delete_checklist'),
    path('core/search_users/', search_users, name='search_users'),
    path('core/invite_member/<int:project_id>/', invite_member, name='invite_member'),
    path('core/get_invites/', get_invites, name='get_invites'),
    path('core/update_invite/<int:invite_id>/', update_invite_status, name='update_invite'),

]
