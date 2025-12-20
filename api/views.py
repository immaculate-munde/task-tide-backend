from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied

from .models import User, Server, ServerMember, Unit, Resource, AssignmentGroup, GroupMember
from .serializers import (
    UserSerializer, ServerSerializer, ServerMemberSerializer, 
    UnitSerializer, ResourceSerializer, AssignmentGroupSerializer, GroupMemberInfoSerializer
)

# --- 1. User Registration View ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# --- 2. Server List & Create View ---
class ServerListCreateView(generics.ListCreateAPIView):
    serializer_class = ServerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Show servers created by the user OR servers the user has joined
        return Server.objects.filter(
            models.Q(created_by=self.request.user) | 
            models.Q(members__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        # SECURITY: Block Students from creating Servers
        if self.request.user.role == 'STUDENT':
            raise PermissionDenied("Students cannot create Servers. Only Class Reps or Lecturers.")
            
        serializer.save(created_by=self.request.user)

# --- 3. Join Server View ---
class JoinServerView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("join_code")
        
        try:
            server = Server.objects.get(join_code=code)
        except Server.DoesNotExist:
            return Response({"error": "Invalid join code"}, status=status.HTTP_404_NOT_FOUND)

        if ServerMember.objects.filter(server=server, user=request.user).exists():
            return Response({"message": "You are already in this server"}, status=status.HTTP_200_OK)

        ServerMember.objects.create(server=server, user=request.user)
        return Response({"message": f"Successfully joined {server.name}"}, status=status.HTTP_201_CREATED)

# --- 4. Unit List & Create View ---
class UnitListCreateView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        server_id = self.request.query_params.get('server_id')
        if server_id:
            return Unit.objects.filter(server_id=server_id)
        return Unit.objects.none()

    def perform_create(self, serializer):
        # SECURITY: Block Students from creating Units
        if self.request.user.role == 'STUDENT':
            raise PermissionDenied("Students cannot create Units. Ask your Class Rep or Lecturer.")
            
        serializer.save(created_by=self.request.user)

# --- 5. Resource List & Create View (File Uploads) ---
class ResourceListCreateView(generics.ListCreateAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        unit_id = self.request.query_params.get('unit_id')
        if unit_id:
            return Resource.objects.filter(unit_id=unit_id)
        return Resource.objects.none()

    def perform_create(self, serializer):
        # SECURITY: Block Students from uploading files
        if self.request.user.role == 'STUDENT':
            raise PermissionDenied("Students cannot upload resources.")

        serializer.save(uploaded_by=self.request.user)

# --- 6. Groups (Class Rep Logic) ---
class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = AssignmentGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        unit_id = self.request.query_params.get('unit_id')
        if unit_id:
            return AssignmentGroup.objects.filter(unit_id=unit_id)
        return AssignmentGroup.objects.none()

    def perform_create(self, serializer):
        # SECURITY: Only Class Reps (or Admins) can create groups
        if self.request.user.role != 'CLASS_REP' and not self.request.user.is_superuser:
            raise PermissionDenied("Only Class Representatives are allowed to create groups.")
        
        serializer.save(created_by=self.request.user)

class JoinGroupView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        group = get_object_or_404(AssignmentGroup, pk=pk)
        
        # LOGIC: Check the specific limit set for THIS group
        current_count = group.members.count()
        limit = group.max_members

        if current_count >= limit:
            return Response(
                {"error": f"This group is full (Max {limit} members reached)."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if GroupMember.objects.filter(group=group, user=request.user).exists():
            return Response({"message": "You are already in this group"}, status=status.HTTP_200_OK)

        GroupMember.objects.create(group=group, user=request.user)
        return Response({"message": f"Successfully joined {group.name}"}, status=status.HTTP_201_CREATED)