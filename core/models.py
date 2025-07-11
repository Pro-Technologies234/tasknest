from django.db import models
from authentication.models import CustomUser
from django.utils.text import slugify

User = CustomUser

def generate_unique_slug(model, field_value, slug_field="slug"):
    base_slug = slugify(field_value)
    slug = base_slug
    counter = 1

    while model.objects.filter(**{slug_field: slug}).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

# Create your models here.
class Project(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects", blank=True, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='project_members')
    background_image = models.ImageField(upload_to='project_backgrounds/', blank=True, null=True)
    archived = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Project, self.title)
        super().save(*args, **kwargs)

class Column(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='column')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Column, self.title)
        super().save(*args, **kwargs)
        


class Task(models.Model):
    PRIORITY = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High')
    ]
    
    STATUS = [
        ('pending', 'Pending'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ManyToManyField(User, blank=True, related_name='assigned_members')
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY, blank=True, null=True, default='low')
    status = models.CharField(max_length=20, choices=STATUS, blank=True, null=True, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Task, self.title)
        super().save(*args, **kwargs)
        
    
    def __str__(self):
        return self.title
        

class CheckList(models.Model):
    title = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='check_lists')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, blank=True, null=True, related_name='check_lists')
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class ProjectInvite(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_users')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='invites')
    status = models.CharField(max_length=20, choices=STATUS, blank=True, null=True, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    
    