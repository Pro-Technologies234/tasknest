from django.shortcuts import render
from .serializers import ProjectSerializer, ColumnSerializer, TaskSerializer, CheckListSerializer, ProjectInviteSerializer
from authentication.serializers import CustomUserSerializer
from authentication.models import CustomUser
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import  MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Column, Task, CheckList, ProjectInvite
from drf_yasg.utils import swagger_auto_schema
# Create your views here.
@swagger_auto_schema(method='post', request_body=ProjectSerializer, responses={201: ProjectSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    
    if serializer.is_valid():
        project = serializer.save(owner=request.user)  # save() returns the model instance
        data = {
            'details': f'Project {project.title} Created Successfully',
            'project': ProjectSerializer(project).data  # optional: return full project data
        }
        return Response(data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=400)

@swagger_auto_schema(method='get', responses={201: ProjectSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_projects(request):
    projects = Project.objects.filter(owner=request.user)
    serializer = ProjectSerializer(projects, many=True)
    if not projects.exists():
        return Response({ 'details' : 'Projects Not Found' },status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data,status=status.HTTP_200_OK)
    
    
@swagger_auto_schema(method='get', responses={200: ProjectSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invited_projects(request):
    projects = Project.objects.filter(members=request.user)
    serializer = ProjectSerializer(projects, many=True)
    if not projects.exists():
        return Response({ 'details' : 'Projects Not Found' },status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data,status=status.HTTP_200_OK)
    
    
@api_view(['PATCH'])  # instead of 'PUT'
@permission_classes([IsAuthenticated])
def update_project(request):
    project_id = request.data.get('id')
    if not project_id:
        return Response({'details': 'Project ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Project.objects.get(id=project_id, owner=request.user)
    except Project.DoesNotExist:
        return Response({'details': 'Project Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project, data=request.data, partial=True)  # partial=True allows partial updates
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', responses={200: ProjectSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, project_id):
    try:
        project_by_owner = Project.objects.filter(id=project_id, owner=request.user).exists()
        
        if project_by_owner:
            project = Project.objects.get(id=project_id, owner=request.user)
        else:
            project = Project.objects.get(id=project_id, members=request.user)
    except Project.DoesNotExist:
        return Response({'details': 'Project Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_invited_project(request, invited_project_id):
    try:
        project
        project = Project.objects.get(id=invited_project_id, members=request.user)
    except Project.DoesNotExist:
        return Response({'details': 'Project Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProjectSerializer(project)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({ 'details': 'Project with that id does not exist' }, status=status.HTTP_404_NOT_FOUND)
    
    project.delete()
    return Response({ 'delete': 'Project has been Deleted Successfully' }, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_column(request, project_id):
    serializer = ColumnSerializer(data=request.data)
    
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'details': 'Project Doeas not Exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if serializer.is_valid():
        serializer.save(project=project)
        return Response({'details': f'Task Column created for {project.title}'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project_columns(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return Response({'details': 'Project Doeas not Exist'}, status=status.HTTP_404_NOT_FOUND)
    columns = Column.objects.filter(project=project)
    serializer = ColumnSerializer(columns, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_column(request, column_id):
    try:
        column = Column.objects.get(id=column_id)
    except Column.DoesNotExist:
        return Response({'details': 'Column Not Found'}, status=status.HTTP_404_NOT_FOUND)
    column.delete()
    return Response({'details': 'Task Column deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request, column_id):
    try:
       column = Column.objects.get(id=column_id) 
    except Column.DoesNotExist:
        return Response({'details': 'Column does not exist'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TaskSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(column=column)
        return Response({'details':'Task Created Succeessfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tasks(request, column_id):
    try:
       column = Column.objects.get(id=column_id) 
    except Column.DoesNotExist:
        return Response({'details': 'Column does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    tasks = Task.objects.filter(column=column)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:  # ✅ Correct model
        return Response({'details': 'Task Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request,task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'details': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_checklist(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'details': 'Task with that id does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CheckListSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(task=task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_checklists(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'details': 'Task with that id does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    check_lists = CheckList.objects.filter(task=task)
    
    serializer = CheckListSerializer(check_lists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_checklist(request, checklist_id):
    try:
        checklist = CheckList.objects.get(id=checklist_id)
    except CheckList.DoesNotExist:
        return Response({'details': 'Checklist not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CheckListSerializer(checklist, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_checklist(request, checklist_id):
    try:
        checklist = CheckList.objects.get(id=checklist_id)
    except CheckList.DoesNotExist:
        return Response({'details': f'Check list with this id {checklist_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    checklist.delete()
    return Response({'details': 'Checklist has been deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users(request):
    query = request.GET.get('q', '')

    users = CustomUser.objects.filter(email__icontains=query)[:10]
    serializer = CustomUserSerializer(users, many=True)

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=ProjectInviteSerializer, responses={201: ProjectInviteSerializer})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_member(request, project_id):
    try:
        project = Project.objects.get(id=project_id)  # fixed: use `id`, not `project_id`
    except Project.DoesNotExist:
        return Response({'detail': 'Project with that ID does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    
    email = request.data.get('email')
    
    if email == request.user.email:
        return Response({'detail': 'You are already a member.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not email:
        return Response({'detail': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'detail': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    # Prevent duplicate invite
    if ProjectInvite.objects.filter(project=project, invited_user=user).exists():
        return Response({'detail': 'User has already been invited to this project.'}, status=status.HTTP_400_BAD_REQUEST)

    # We don't pass all fields from request.data — we manually set them
    serializer = ProjectInviteSerializer(data={})
    if serializer.is_valid():
        serializer.save(invited_user=user, project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', responses={201: ProjectInviteSerializer})
@api_view(['GET'])
@swagger_auto_schema()
def get_invites(request):
    invited_user = request.user
    invites = ProjectInvite.objects.filter(invited_user=invited_user)
    project_invites = ProjectInviteSerializer(invites, many=True)
    return Response(project_invites.data, status=status.HTTP_200_OK)



@swagger_auto_schema(method='patch', request_body=ProjectInviteSerializer, responses={200: ProjectInviteSerializer})
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_invite_status(request, invite_id):
    try:
        invite = ProjectInvite.objects.get(id=invite_id, invited_user=request.user)
    except ProjectInvite.DoesNotExist:
        return Response({'detail': 'Invite not found or unauthorized.'}, status=status.HTTP_404_NOT_FOUND)


    status_choice = request.data.get("status")
    if status_choice not in ["accepted", "rejected"]:
        return Response({"detail": "Invalid status choice."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ProjectInviteSerializer(invite, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        if status_choice == "accepted":
            invite.project.members.add(request.user)  # assumes `members = models.ManyToManyField(User, ...)`
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

