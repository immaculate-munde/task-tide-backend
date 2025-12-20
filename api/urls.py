from django.urls import path
from .views import RegisterView, ServerListCreateView, JoinServerView, UnitListCreateView, ResourceListCreateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Auth Routes
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),      
    
    # Server Routes
    path('servers/', ServerListCreateView.as_view(), name='server-list-create'),
    path('servers/join/', JoinServerView.as_view(), name='join-server'),
    
    # Units & Resources
    path('units/', UnitListCreateView.as_view(), name='unit-list-create'),
    path('resources/', ResourceListCreateView.as_view(), name='resource-list-create'),
]