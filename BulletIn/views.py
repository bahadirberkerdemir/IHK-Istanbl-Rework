from django.shortcuts import render,redirect
from . import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout

# Create your views here.

@login_required(login_url='/login')
def showBulletin(request):
    return render(request, 'BulletIn/BulletIn.html')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'degistir.html'
    success_url = reverse_lazy('login') # Değiştirildi: Başarılı değişim sonrası yönlendirilecek sayfa login olarak ayarlandı

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request) # Değiştirildi: Şifre başarıyla değiştirildikten sonra oturum (logout) sonlandırıldı
        return response