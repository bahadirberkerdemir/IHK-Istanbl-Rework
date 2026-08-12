from django.contrib import admin

from django.contrib import admin
from persons.models import Hakem,Gozlemci
from .forms import HakemForm, GozlemciForm

"""class HakemAdmin(admin.ModelAdmin):
   form = HakemForm # Değiştirildi: ModelBir için formu bağladık

class GozlemciAdmin(admin.ModelAdmin):
    form = GozlemciForm # Değiştirildi: ModelIki için formu bağladık"""

admin.site.register(Hakem)
admin.site.register(Gozlemci)