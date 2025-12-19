from rest_framework import serializers
from .models import User, Server, ServerMember

# --- 1. User Serializer (For Registration) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}} # Don't show password in responses

    def create(self, validated_data):
        # We override create to handle password hashing automatically
        user = User.objects.create_user(**validated_data)
        return user

# --- 2. Server Serializer (For creating/viewing classrooms) ---
class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ['id', 'name', 'join_code', 'description', 'created_by', 'created_at']
        read_only_fields = ['join_code', 'created_by', 'created_at'] # These are auto-generated

# --- 3. Server Member Serializer (For listing who is in a class) ---
class ServerMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username') # Show name, not just ID
    server_name = serializers.ReadOnlyField(source='server.name')

    class Meta:
        model = ServerMember
        fields = ['id', 'user_name', 'server_name', 'joined_at']