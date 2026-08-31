from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HakemProfilForm, GozlemciProfilForm
from .models import Gozlemci, Hakem

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


def _turkce_anahtar(metin):
    ceviri = str.maketrans('IİıĞğÜüŞşÖöÇç', 'iiigguussoocc')
    return (metin or '').translate(ceviri).lower()


def _ilk_ad(ad_soyad):
    if not ad_soyad:
        return ''
    return ad_soyad.strip().split()[0]


@login_required(login_url='/login')
def kisi_arama_view(request):
    arama = request.GET.get('q', '').strip()
    hakemler = Hakem.objects.all()
    gozlemciler = Gozlemci.objects.all()
    if arama:
        hakemler = hakemler.filter(ad_soyad__icontains=arama)
        gozlemciler = gozlemciler.filter(ad_soyad__icontains=arama)

    kisiler = []
    for hakem in hakemler:
        kisiler.append({
            'ad_soyad': hakem.ad_soyad,
            'telefon': hakem.telefon_cep,
            'klasman': hakem.get_klasman_display(),
            'lisans_no': hakem.lisans_no,
            'tip': 'Hakem',
        })
    for gozlemci in gozlemciler:
        kisiler.append({
            'ad_soyad': gozlemci.ad_soyad,
            'telefon': gozlemci.telefon_cep,
            'klasman': gozlemci.get_klasman_display(),
            'lisans_no': gozlemci.lisans_no,
            'tip': 'Gözlemci',
        })

    kisiler.sort(key=lambda k: _turkce_anahtar(_ilk_ad(k['ad_soyad'])))
    sayfa_no = request.GET.get('sayfa', 1)
    sayfalayici = Paginator(kisiler, 15)
    sayfa = sayfalayici.get_page(sayfa_no)
    return render(request, 'persons/kisi_arama.html', {
        'sayfa': sayfa,
        'arama': arama,
    })