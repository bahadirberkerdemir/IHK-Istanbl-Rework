from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Person, Hakem, Gozlemci


class GirisFormu(AuthenticationForm):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)


class HakemProfilForm(forms.ModelForm):
    class Meta:
        model = Hakem
        # Adminin gireceği her şeyi formdan KESİNLİKLE çıkarıyoruz
        exclude = ['user', 'gorev', 'klasman', 'lisans_no', 'ad_soyad', 'tckn']
        
        widgets = {
            'ad_soyad': forms.TextInput(attrs={'class': 'form-control'}),
            'tckn': forms.TextInput(attrs={'class': 'form-control'}),
            'lisans_no': forms.NumberInput(attrs={'class': 'form-control'}),
            'klasman': forms.Select(attrs={'class': 'form-select'}),
            'gorev': forms.Select(attrs={'class': 'form-select'}),
            # --- 1. BÖLÜM: ADRES, BANKA VE FİZİKSEL BİLGİLER ---
            'ilce': forms.TextInput(attrs={'class': 'form-control'}),
            'semt': forms.TextInput(attrs={'class': 'form-control'}),
            'kan_grubu': forms.Select(attrs={'class': 'form-select'}),
            'banka': forms.TextInput(attrs={'class': 'form-control'}),
            'sube_kodu': forms.TextInput(attrs={'class': 'form-control'}),
            'hesap_no': forms.TextInput(attrs={'class': 'form-control'}),
            'iban': forms.TextInput(attrs={'class': 'form-control'}),
            
            'boy': forms.NumberInput(attrs={'class': 'form-control'}),
            'kilo': forms.NumberInput(attrs={'class': 'form-control'}),
            'beden': forms.TextInput(attrs={'class': 'form-control'}),
            'ayak_no': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'askerlik_durumu': forms.Select(attrs={'class': 'form-select'}),
            'tecil_tarihi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            # --- 2. BÖLÜM: EĞİTİM BİLGİLERİ ---
            'egitim_seviyesi': forms.Select(attrs={'class': 'form-select'}),
            'mezun_oldugu_okul': forms.TextInput(attrs={'class': 'form-control'}),
            'mezun_oldugu_bolum': forms.TextInput(attrs={'class': 'form-control'}),
            'mezuniyet_yili': forms.NumberInput(attrs={'class': 'form-control'}),

            # --- 3. BÖLÜM: KİMLİK BİLGİLERİ ---
            'anne_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'baba_adi': forms.TextInput(attrs={'class': 'form-control'}),
            'dogum_yeri': forms.TextInput(attrs={'class': 'form-control'}),
            'dogum_tarihi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medeni_hal': forms.Select(attrs={'class': 'form-select'}),
            
            'nufus_il': forms.TextInput(attrs={'class': 'form-control'}),
            'nufus_ilce': forms.TextInput(attrs={'class': 'form-control'}),
            'mahalle_koy': forms.TextInput(attrs={'class': 'form-control'}),
            
            'cilt_no': forms.TextInput(attrs={'class': 'form-control'}),
            'aile_sira_no': forms.TextInput(attrs={'class': 'form-control'}),
            'sira_no': forms.TextInput(attrs={'class': 'form-control'}),
            'cinsiyet': forms.Select(attrs={'class': 'form-select'}),

            # --- DİĞER BİLGİLER (İletişim, Bölge, Fotoğraf vb.) ---
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'bolge': forms.Select(attrs={'class': 'form-select'}),
            'eposta': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefon_cep': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_ev': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_is': forms.TextInput(attrs={'class': 'form-control'}),
            'telefon_dahili': forms.TextInput(attrs={'class': 'form-control'}),
            'meslek': forms.TextInput(attrs={'class': 'form-control'}),

            # --- MÜSAİTLİK GÜNLERİ (Boolean - Checkbox) ---
            'monday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tuesday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wednesday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'thursday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'friday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'saturday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sunday': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        


class GozlemciProfilForm(forms.ModelForm):
    class Meta:
        model = Gozlemci
        # Adminin gireceği her şeyi formdan KESİNLİKLE çıkarıyoruz
        exclude = ['user', 'gorev', 'klasman', 'lisans_no', 'ad_soyad', 'tckn']
        # HakemProfilForm'daki aynı CSS'leri (widgets) kopyalıyoruz:
        widgets = HakemProfilForm.Meta.widgets 
