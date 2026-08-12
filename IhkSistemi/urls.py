"""
URL configuration for IhkSistemi project.

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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from BulletIn.views import CustomPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BulletIn.urls')),
    path('persons/', include('persons.urls')),
    path('', include('django.contrib.auth.urls')),
    path('sifre-degistir/', CustomPasswordChangeView.as_view(template_name='degistir.html'), name='password_change'), 
    path('sifre-degistir/basarili/', auth_views.PasswordChangeDoneView.as_view(template_name='degistir_basarili.html'), name='password_change_done')
]
