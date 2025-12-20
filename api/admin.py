from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Server, ServerMember, Unit, Resource

# Register your models here.

# 1. Register the Custom User Model
admin.site.register(User, UserAdmin)

# 2. Register the Server Model
# FIX: Use 'admin.ModelAdmin', NOT 'admin.site.ModelAdmin'
@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'join_code', 'created_by', 'created_at')
    readonly_fields = ('join_code', 'id')

# 3. Register the ServerMember Model
# FIX: Use 'admin.ModelAdmin', NOT 'admin.site.ModelAdmin'
@admin.register(ServerMember)
class ServerMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'server', 'joined_at')
    
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'server', 'created_by')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'resource_type', 'uploaded_by')