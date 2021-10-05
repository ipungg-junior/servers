from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Pengguna)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Divisi)
admin.site.register(JenisBerkas)
admin.site.register(File)
admin.site.register(SuratMasuk)
admin.site.register(SuratKeluar)
admin.site.register(Arsip)
admin.site.register(Note)
admin.site.register(TemporaryDownload)