"""adminServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from appWeb import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('global/', include(('appWeb.urls','global'))),
    path('login/', views.login, name='login'),
    path('', login_required(views.home,login_url='login'), name='home'), # el login es por que si no redirije a accounts/login que es de django
    path('registro/',views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('monitor/<str:pk>/',login_required(views.monitoreo, login_url='login'), name='monitor')
]
