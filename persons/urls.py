from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'persons'

urlpatterns = [
    path('', views.bilgilerim_view, name='bilgilerim'),
    path('kisi-arama/', views.kisi_arama_view, name='kisi_arama'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)