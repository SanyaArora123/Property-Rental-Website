"""
URL configuration for rentals project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

# urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from myapp import views
from django.contrib.auth.views import LogoutView, LoginView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    
    path('register/', views.register, name='register'),
    path('loginUser/', auth_views.LoginView.as_view(template_name='myapp/loginUser.html'), name='loginUser'),
    path('logOut/', views.logOut, name='logOut'),
    path('become-seller/', views.become_seller, name='become_seller'),
    path('properties/', views.properties_list, name='properties_list'),
    path('search/', views.search, name='search'),
    path('property_detail/<int:Pid>/', views.property_detail, name='property_detail'),
    path('add-property/', views.add_property, name='add_property'),
    
   
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

