from django.shortcuts import render,redirect
from . import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from .forms import HakemProfilForm, GozlemciProfilForm

# Create your views here.

"""@login_required(login_url='/login')
def personinfo(request):
    return render(request, ('persons/bilgilerim.html'))"""


@login_required(login_url='/login')
def bilgilerim_view(request):
    if hasattr(request.user, 'hakem'):
        profil = request.user.hakem
        FormSinifi = HakemProfilForm
    elif hasattr(request.user, 'gozlemci'):
        profil = request.user.gozlemci
        FormSinifi = GozlemciProfilForm
    else:
        return render(request, 'persons/hata.html', {'mesaj': 'Profil bulunamadı.'})

    if request.method == 'POST':
        form = FormSinifi(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('persons:bilgilerim')
    else:
        form = FormSinifi(instance=profil)

    # DİKKAT: 'profil': profil kısmını ekledik ki HTML'de değerleri okuyabilelim
    return render(request, 'persons/bilgilerim.html', {'form': form, 'profil': profil})


@login_required # Sadece giriş yapmış kişiler bu sayfayı görebilir
def profil_guncelle_view(request):
    # 1. Giriş yapan kullanıcının Hakem mi Gözlemci mi olduğunu tespit ediyoruz
    if hasattr(request.user, 'hakem'):
        profil = request.user.hakem
        FormSinifi = HakemProfilForm
    elif hasattr(request.user, 'gozlemci'):
        profil = request.user.gozlemci
        FormSinifi = GozlemciProfilForm
    else:
        # Eğer admin kendisine henüz bir Hakem veya Gözlemci profili atamadıysa:
        return render(request, 'hata.html', {'mesaj': 'Sisteme kayıtlı bir personel profiliniz bulunamadı.'})

    # 2. Form işlemleri (Kaydetme veya Gösterme)
    if request.method == 'POST':
        # instance=profil parametresi, kullanıcının mevcut verilerinin üzerine yazılmasını sağlar
        form = FormSinifi(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.save()
            return redirect('profil_guncelle') # Başarılıysa aynı sayfaya geri yönlendir (veya başka bir URL adı yaz)
    else:
        form = FormSinifi(instance=profil)

    # 3. Formu HTML şablonuna gönder
    return render(request, 'profil_guncelle.html', {'form': form})