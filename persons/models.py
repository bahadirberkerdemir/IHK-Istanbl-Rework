from django.db import models
from PIL import Image,ImageOps
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.



class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='%(class)s', null=True, blank=True)
    exact_digits = RegexValidator(
        regex=r'^\d{11}$', 
        message='Bu alan tam olarak 11 haneli bir sayı olmalıdır.'
    )

    
    bolge_list = [('ANA','Anadolu'), ('AV1','Avrupa-1'),
                  ('AV2','Avrupa-2')]

    BLOOD_GROUPS = [
        ('0_RH_POS', '0 RH+'),
        ('0_RH_NEG', '0 RH-'),
        ('A_RH_POS', 'A RH+'),
        ('A_RH_NEG', 'A RH-'),
        ('B_RH_POS', 'B RH+'),
        ('B_RH_NEG', 'B RH-'),
        ('AB_RH_POS', 'AB RH+'),
        ('AB_RH_NEG', 'AB RH-'),
    ]

    MILITARY_STATUS = [
        ('TECILLI', 'Tecilli'),
        ('YAPTI', 'Yaptı'),
        ('MUAF', 'Muaf'),
    ]

    EDUCATION_LEVELS = [
        ('ILKOKUL', 'İlkokul'),
        ('ORTAOKUL', 'Ortaokul'),
        ('LISE', 'Lise'),
        ('ONLISANS', 'Önlisans'),
        ('LISANS', 'Lisans'),
        ('YUKSEK_LISANS', 'Yüksek Lisans'),
        ('DOKTORA', 'Doktora'),
    ]

    MARITAL_STATUS = [
        ('BEKAR', 'Bekar'),
        ('EVLI', 'Evli'),
    ]

    GENDER_CHOICES = [
        ('ERKEK', 'Erkek'),
        ('KADIN', 'Kadın'),
    ]

    # --- 1. BÖLÜM: ADRES, BANKA VE FİZİKSEL BİLGİLER ---
    ilce = models.CharField(max_length=100, verbose_name="İlçe", null=True, blank=True)
    semt = models.CharField(max_length=100, verbose_name="Semt", null=True, blank=True)
    kan_grubu = models.CharField(max_length=10, choices=BLOOD_GROUPS, verbose_name="Kan Grubu", null=True, blank=True)
    banka = models.CharField(max_length=100, verbose_name="Banka", null=True, blank=True)
    sube_kodu = models.CharField(max_length=20, verbose_name="Şube Kodu", null=True, blank=True)
    hesap_no = models.CharField(max_length=50, verbose_name="Hesap No", null=True, blank=True)
    iban = models.CharField(max_length=34, verbose_name="IBAN", null=True, blank=True)
    
    boy = models.PositiveIntegerField(null=True, blank=True, verbose_name="Boy (cm)")
    kilo = models.PositiveIntegerField(null=True, blank=True, verbose_name="Kilo (kg)")
    beden = models.CharField(max_length=10, null=True, blank=True, verbose_name="Beden")
    ayak_no = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ayak No")
    
    askerlik_durumu = models.CharField(max_length=20, choices=MILITARY_STATUS, verbose_name="Askerlik Durumu", null=True, blank=True)
    tecil_tarihi = models.DateField(null=True, blank=True, verbose_name="Tecil Tarihi")

    # --- 2. BÖLÜM: EĞİTİM BİLGİLERİ ---
    egitim_seviyesi = models.CharField(max_length=20, choices=EDUCATION_LEVELS, verbose_name="Eğitim Seviyesi", null=True, blank=True)
    mezun_oldugu_okul = models.CharField(max_length=255, verbose_name="Mezun Olduğu Okul Adı", null=True, blank=True)
    mezun_oldugu_bolum = models.CharField(max_length=255, null=True, blank=True, verbose_name="Mezun Olduğu Bölüm")
    mezuniyet_yili = models.PositiveIntegerField(verbose_name="Mezuniyet Yılı", null=True, blank=True)

    # --- 3. BÖLÜM: KİMLİK BİLGİLERİ ---
    anne_adi = models.CharField(max_length=100, verbose_name="Anne Adı", null=True, blank=True)
    baba_adi = models.CharField(max_length=100, verbose_name="Baba Adı", null=True, blank=True)
    dogum_yeri = models.CharField(max_length=100, verbose_name="Doğum Yeri", null=True, blank=True)
    dogum_tarihi = models.DateField(verbose_name="Doğum Tarihi", null=True, blank=True)
    medeni_hal = models.CharField(max_length=10, choices=MARITAL_STATUS, verbose_name="Medeni Hal", null=True, blank=True)
    
    nufus_il = models.CharField(max_length=100, verbose_name="İl (Nüfus)", null=True, blank=True)
    nufus_ilce = models.CharField(max_length=100, verbose_name="İlçe (Nüfus)", null=True, blank=True)
    mahalle_koy = models.CharField(max_length=150, verbose_name="Mahalle/Köy", null=True, blank=True)
    
    cilt_no = models.CharField(max_length=20, verbose_name="Cilt No", null=True, blank=True)
    aile_sira_no = models.CharField(max_length=20, verbose_name="Aile Sıra No", null=True, blank=True)
    sira_no = models.CharField(max_length=20, verbose_name="Sıra No", null=True, blank=True)
    cinsiyet = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Cinsiyet", null=True, blank=True)

    foto = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='Fotograf')
    gorev = models.CharField(max_length=12, choices=[('Hakem','Hakem'),('Gözlemci','Gözlemci')], verbose_name='Gorev', null=True, blank=True)
    #klasman = models.CharField(max_length=50, choices=kisi_klasman)
    lisans_no = models.IntegerField(null=True, blank=True, verbose_name='Lisans No')
    bolge = models.CharField(max_length=16, choices=bolge_list,verbose_name='Bolge', null=True, blank=True)
    ad_soyad = models.CharField(max_length=100,verbose_name='Ad Soyad', null=True, blank=True)
    tckn = models.CharField(max_length=11, validators=[exact_digits], verbose_name='Kimlik No', null=True, blank=True)
    eposta = models.EmailField(max_length=100,verbose_name='Eposta', null=True, blank=True)
    telefon_cep =  models.CharField(max_length=24,verbose_name='Cep No', null=True, blank=True)
    telefon_ev = models.CharField(max_length=24, null=True, blank=True, verbose_name='Ev Telefon No')
    telefon_is = models.CharField(max_length=24, null=True, blank=True, verbose_name='İş Telefon No')
    telefon_dahili = models.CharField(max_length=24, null=True, blank=True, verbose_name='Dahili Telefon No')

    meslek = models.CharField(max_length=64, null=True, blank=True, verbose_name='Meslek')
    monday = models.BooleanField(default=False, verbose_name="Pazartesi")
    tuesday = models.BooleanField(default=False, verbose_name="Salı")
    wednesday = models.BooleanField(default=False, verbose_name="Çarşamba")
    thursday = models.BooleanField(default=False, verbose_name="Perşembe")
    friday = models.BooleanField(default=False, verbose_name="Cuma")
    saturday = models.BooleanField(default=False, verbose_name="Cumartesi")
    sunday = models.BooleanField(default=False, verbose_name="Pazar")


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.foto:
            img = Image.open(self.foto.path) # Değiştirildi: profile_image yerine foto yazıldı
            
            target_size = (1000, 1000)
            img = ImageOps.fit(img, target_size, Image.Resampling.LANCZOS)
            
            img.save(self.foto.path) # Değiştirildi: profile_image yerine foto yazıldı

    class Meta:
        abstract = True




class Hakem(Person):
    hakem_klasman = [('YAH','Yeni Aday Hakem'),('AH','Aday Hakem'),
                             ('IL','İl Hakemi'),('BYH','BYH'),('KBYH','KBYH'), ('BH','BH'),
                             ('KBH','KBH'),('KH','KH'),('KYH','KYH'),('ÜKH','ÜKH'),('ÜKYH','ÜKYH'),
                               ('VAR','VAR')] 
    klasman = models.CharField(max_length=50, verbose_name="Hakem Klasmanı", choices=hakem_klasman)
    

    def __str__(self):
        return f"Hakem: {self.ad_soyad} ({self.klasman})"


class Gozlemci(Person):
    gozlemci_klasman = [('IL','İl Gözlemcisi'),
                        ('BG','BG'),('KG','KG'),('ÜKG','ÜKG')]
    klasman = models.CharField(default=0, verbose_name="Klasman", choices=gozlemci_klasman)
   
    def __str__(self):
        return f"Gözlemci: {self.ad_soyad} ({self.klasman})"

