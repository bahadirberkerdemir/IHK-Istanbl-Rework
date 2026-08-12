from django.urls import path
from . import views
app_name = 'BulletIn'

urlpatterns = [
    path('', views.showBulletin, name='showBulletin'), 
]