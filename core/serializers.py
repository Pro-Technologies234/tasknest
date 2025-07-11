from rest_framework import serializers
from .models import Project, Column, Task, CheckList, ProjectInvite
from authentication.serializers import CustomUserSerializer
from authentication.models import CustomUser
class ProjectSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer(read_only=True)
    members = CustomUserSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = [
            'id',
            'slug',
            'owner',
            'members',
            'title', 
            'description',
            'archived',
            'favourite',
            'background_image',
        ]
        read_only_fields = ['id', 'slug', 'owner', 'members']  # Prevent users from passing these in request
        
class ColumnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Column
        fields = [
            'id',
            'title',
            'created_at',
        ]
        

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = CustomUserSerializer(many=True, read_only=True)
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.all(),
        write_only=True,
        source="assigned_to"
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'priority',
            'status',
            'due_date',
            'assigned_to',
            'assigned_to_ids',
            'created_at',
        ]
        
class CheckListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CheckList
        fields = [
            'id',
            'title',
            'assigned_to',
            'checked',
        ]
        
        
class ProjectInviteSerializer(serializers.ModelSerializer):
    
    project = ProjectSerializer(read_only=True)
    
    class Meta:
        model = ProjectInvite
        fields = ['id', 'invited_user', 'project', 'status', 'created_at']
        read_only_fields = ['invited_user', 'project', 'created_at']