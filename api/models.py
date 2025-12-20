from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import random
import string

# --- Custom User Model ---
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CLASSREP = "CLASSREP", "Class Rep"
        LECTURER = "LECTURER", "Lecturer"
        STUDENT = "STUDENT", "Student"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    
    # Resolving conflict with default Django user groups/permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

# --- Helper: Generate Join Code ---
def generate_join_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- Server Model ---
class Server(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    # Automatically generate a code like 'A7X29B'
    join_code = models.CharField(max_length=6, default=generate_join_code, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_servers')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} [{self.join_code}]"

# --- Server Members (Who is in which server) ---
class ServerMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_servers')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('server', 'user') # Prevent joining twice

    def __str__(self):
        return f"{self.user.username} -> {self.server.name}"
    
    # --- Unit Model (Subjects) ---
class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=100) # e.g. "Calculus I"
    code = models.CharField(max_length=20)   # e.g. "MAT101"
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_units')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

# --- Resource Model (File Uploads) ---
class Resource(models.Model):
    class Type(models.TextChoices):
        DOCUMENT = "DOCUMENT", "Document"
        ASSIGNMENT = "ASSIGNMENT", "Assignment"
        PAST_PAPER = "PAST_PAPER", "Past Paper"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resources/') # <--- This handles the upload
    resource_type = models.CharField(max_length=50, choices=Type.choices, default=Type.DOCUMENT)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_resources')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title