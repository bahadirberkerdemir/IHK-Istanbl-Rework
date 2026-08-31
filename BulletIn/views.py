from collections import OrderedDict

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Mac


def _kullanici_profil(user):
    if hasattr(user, 'hakem'):
        return user.hakem, 'hakem'
    if hasattr(user, 'gozlemci'):
        return user.gozlemci, 'gozlemci'
    return None, None


def _mac_queryset():
    return Mac.objects.select_related(
        'hakem',
        'birinci_yardimci',
        'ikinci_yardimci',
        'dorduncu_hakem',
        'gozlemci',
    ).order_by('tarih_saat')


def _kullanici_maclari(profil, tip):
    qs = _mac_queryset()
    if tip == 'hakem':
        return qs.filter(
            Q(hakem=profil)
            | Q(birinci_yardimci=profil)
            | Q(ikinci_yardimci=profil)
            | Q(dorduncu_hakem=profil)
        )
    if tip == 'gozlemci':
        return qs.filter(gozlemci=profil)
    return qs.none()


def _gunlere_gore_grupla(maclar, kullanici_mac_idler=None):
    kullanici_mac_idler = kullanici_mac_idler or set()
    gruplar = OrderedDict()
    for mac in maclar:
        gun = timezone.localtime(mac.tarih_saat).date()
        gruplar.setdefault(gun, []).append(mac)

    def sirala_satirlar(satirlar):
        if not kullanici_mac_idler:
            return satirlar
        benim = [m for m in satirlar if m.id in kullanici_mac_idler]
        diger = [m for m in satirlar if m.id not in kullanici_mac_idler]
        return benim + diger

    kullanici_gunleri = set()
    for mac in maclar:
        if mac.id in kullanici_mac_idler:
            kullanici_gunleri.add(timezone.localtime(mac.tarih_saat).date())

    benim_bloklar = []
    diger_bloklar = []
    for gun, satirlar in gruplar.items():
        blok = {'gun': gun, 'maclar': sirala_satirlar(satirlar)}
        if gun in kullanici_gunleri:
            benim_bloklar.append(blok)
        else:
            diger_bloklar.append(blok)
    return benim_bloklar + diger_bloklar


@login_required(login_url='/login')
def showBulletin(request):
    profil, tip = _kullanici_profil(request.user)
    kullanici_mac_idler = set()
    if profil:
        kullanici_mac_idler = set(_kullanici_maclari(profil, tip).values_list('id', flat=True))

    gun_bloklari = _gunlere_gore_grupla(_mac_queryset(), kullanici_mac_idler)
    return render(request, 'BulletIn/BulletIn.html', {
        'gun_bloklari': gun_bloklari,
        'rapor_butonu_goster': False,
        'orta_hakem_id': None,
        'kullanici_hakem_id': profil.id if tip == 'hakem' else None,
        'kullanici_gozlemci_id': profil.id if tip == 'gozlemci' else None,
    })


@login_required(login_url='/login')
def maclarim(request):
    profil, tip = _kullanici_profil(request.user)
    if not profil:
        return render(request, 'persons/hata.html', {
            'mesaj': 'Sisteme kayıtlı bir hakem veya gözlemci profiliniz bulunamadı.',
        })

    orta_hakem_id = profil.id if tip == 'hakem' else None

    if request.method == 'POST' and tip == 'hakem':
        mac = get_object_or_404(Mac, pk=request.POST.get('mac_id'))
        if mac.hakem_id == profil.id and not mac.hakem_raporu_gonderildi:
            mac.hakem_raporu_gonderildi = True
            mac.save(update_fields=['hakem_raporu_gonderildi'])
        return redirect('BulletIn:maclarim')

    gun_bloklari = _gunlere_gore_grupla(_kullanici_maclari(profil, tip))
    return render(request, 'BulletIn/maclarim.html', {
        'gun_bloklari': gun_bloklari,
        'rapor_butonu_goster': True,
        'orta_hakem_id': orta_hakem_id,
        'kullanici_hakem_id': profil.id if tip == 'hakem' else None,
        'kullanici_gozlemci_id': profil.id if tip == 'gozlemci' else None,
    })


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'degistir.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response
