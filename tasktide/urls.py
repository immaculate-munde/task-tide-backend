"""
URL configuration for tasktide project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def home_view(request):
    return render(request, 'index.html')
def create_admin_backdoor(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        return HttpResponse("✅ SUCCESS: User 'admin' created! Password: 'admin123'")
    return HttpResponse("⚠️ User 'admin' already exists.")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('make-admin/', create_admin_backdoor),
    # This uses the standard Django login page (looks like Admin but for everyone)
    path('test-login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='test_login'),
    path('api/', include('api.urls')),
    path('api/auth/', include('rest_framework.urls')), # <--- Added for browsable API login/logout 
    path('api-auth/', include('rest_framework.urls')),
    
]
# This allows you to see uploaded files while running on localhost
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
