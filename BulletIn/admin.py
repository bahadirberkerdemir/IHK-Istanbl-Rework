from django.contrib import admin

from persons.models import Gozlemci, Hakem
from .models import Mac


@admin.register(Hakem)
class HakemAdmin(admin.ModelAdmin):
    search_fields = ('ad_soyad', 'lisans_no', 'tckn')
    list_display = ('ad_soyad', 'klasman', 'lisans_no', 'telefon_cep')


@admin.register(Gozlemci)
class GozlemciAdmin(admin.ModelAdmin):
    search_fields = ('ad_soyad', 'lisans_no', 'tckn')
    list_display = ('ad_soyad', 'klasman', 'lisans_no', 'telefon_cep')


@admin.register(Mac)
class MacAdmin(admin.ModelAdmin):
    list_display = (
        'tarih_saat',
        'ev_sahibi',
        'deplasman',
        'lig',
        'hakem',
        'gozlemci',
        'hakem_sayisi',
    )
    list_filter = ('lig', 'hakem_sayisi')
    search_fields = ('ev_sahibi', 'deplasman', 'lig')
    autocomplete_fields = (
        'hakem',
        'birinci_yardimci',
        'ikinci_yardimci',
        'dorduncu_hakem',
        'gozlemci',
    )
    fieldsets = (
        ('Maç Bilgileri', {
            'fields': ('tarih_saat', 'ev_sahibi', 'deplasman', 'lig', 'hakem_sayisi'),
        }),
        ('Görevli Hakemler', {
            'fields': ('hakem', 'birinci_yardimci', 'ikinci_yardimci', 'dorduncu_hakem', 'gozlemci'),
        }),
        ('Rapor ve Puan', {
            'fields': ('hakem_raporu_gonderildi', 'gozlemci_puani', 'gozlemci_raporu'),
        }),
    )
