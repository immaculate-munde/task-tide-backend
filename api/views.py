from django.db import models
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Server, ServerMember, Unit, Resource
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, ServerSerializer, ServerMemberSerializer, UnitSerializer, ResourceSerializer

# --- 1. User Registration View ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Anyone can register

# --- 2. Server List & Create View ---
class ServerListCreateView(generics.ListCreateAPIView):
    serializer_class = ServerSerializer
    permission_classes = [permissions.IsAuthenticated] # Must be logged in

    def get_queryset(self):
        # Show servers created by the user OR servers the user has joined
        return Server.objects.filter(models.Q(created_by=self.request.user) | models.Q(members__user=self.request.user)).distinct()

    def perform_create(self, serializer):
        # Automatically set the "created_by" field to the current user
        serializer.save(created_by=self.request.user)

# --- 3. Join Server View (The "Magic Code" Logic) ---
class JoinServerView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("join_code")
        
        # 1. Check if server exists
        try:
            server = Server.objects.get(join_code=code)
        except Server.DoesNotExist:
            return Response({"error": "Invalid join code"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Check if already a member
        if ServerMember.objects.filter(server=server, user=request.user).exists():
            return Response({"message": "You are already in this server"}, status=status.HTTP_200_OK)

        # 3. Add to server
        ServerMember.objects.create(server=server, user=request.user)
        return Response({"message": f"Successfully joined {server.name}"}, status=status.HTTP_201_CREATED)

# --- 4. Unit List & Create View ---
class UnitListCreateView(generics.ListCreateAPIView):
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow filtering by server ID: /api/units/?server_id=123
        server_id = self.request.query_params.get('server_id')
        if server_id:
            return Unit.objects.filter(server_id=server_id)
        return Unit.objects.none() # Return nothing if no server specified

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# --- 5. Resource List & Create View (File Uploads) ---
class ResourceListCreateView(generics.ListCreateAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) # <--- ENABLE FILE UPLOADS

    def get_queryset(self):
        # Allow filtering by unit ID: /api/resources/?unit_id=123
        unit_id = self.request.query_params.get('unit_id')
        if unit_id:
            return Resource.objects.filter(unit_id=unit_id)
        return Resource.objects.none()

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)