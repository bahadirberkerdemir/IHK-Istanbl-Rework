from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from persons.models import Hakem, Gozlemci


class Mac(models.Model):
    HAKEM_SAYISI = [
        (1, 'Tek hakem'),
        (3, 'Üç hakem'),
        (4, 'Dört hakem'),
    ]

    tarih_saat = models.DateTimeField(verbose_name='Maç Tarihi ve Saati')
    ev_sahibi = models.CharField(max_length=150, verbose_name='Ev Sahibi')
    deplasman = models.CharField(max_length=150, verbose_name='Deplasman')
    lig = models.CharField(max_length=150, verbose_name='Lig')
    hakem_sayisi = models.PositiveSmallIntegerField(
        choices=HAKEM_SAYISI,
        default=3,
        verbose_name='Hakem Sayısı',
    )

    hakem = models.ForeignKey(
        Hakem,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orta_hakem_maclari',
        verbose_name='Hakem',
    )
    birinci_yardimci = models.ForeignKey(
        Hakem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='birinci_yardimci_maclari',
        verbose_name='1. Yardımcı Hakem',
    )
    ikinci_yardimci = models.ForeignKey(
        Hakem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ikinci_yardimci_maclari',
        verbose_name='2. Yardımcı Hakem',
    )
    dorduncu_hakem = models.ForeignKey(
        Hakem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dorduncu_hakem_maclari',
        verbose_name='Dördüncü Hakem',
    )
    gozlemci = models.ForeignKey(
        Gozlemci,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='gozlemci_maclari',
        verbose_name='Gözlemci',
    )

    hakem_raporu_gonderildi = models.BooleanField(
        default=False,
        verbose_name='Hakem Raporu Gönderildi',
    )
    gozlemci_puani = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Gözlemci Puanı',
    )
    gozlemci_raporu = models.FileField(
        upload_to='gozlemci_raporlari/',
        null=True,
        blank=True,
        verbose_name='Gözlemci Raporu',
    )

    class Meta:
        verbose_name = 'Maç'
        verbose_name_plural = 'Maçlar'
        ordering = ['tarih_saat']

    def __str__(self):
        return f'{self.ev_sahibi} - {self.deplasman} ({self.tarih_saat})'

    def mac_saati_gecti(self):
        return timezone.now() >= self.tarih_saat

    def gozlemci_raporu_gorunur(self):
        return self.mac_saati_gecti() and bool(self.gozlemci_raporu)
