from django.db import models
from django.db.models.fields import BooleanField
from django.utils import timezone

# Tabel Departemen
class Department(models.Model):
    departementID = models.CharField(max_length=6, null=False)
    departementName = models.CharField(max_length=21, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    url = models.CharField(null=True, max_length=40)
    status = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.departementName

# Tabel Divisi
class Divisi(models.Model):
    divisiID = models.CharField(max_length=6, null=False)
    divisiName = models.CharField(max_length=21, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    url = models.CharField(null=True, max_length=40)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        department = str(self.department)
        return (f'{self.divisiName} - {department}')

# Tabel Role Karyawan (Staff, Manajer, dll)
class Role(models.Model):
    roleCode = models.CharField(max_length=4, null=False)
    roleName = models.CharField(max_length=16, null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.roleName

# Tabel Jenis Berkas (Dinas, Selebaran, dll)
class JenisBerkas(models.Model):
    jenisCode = models.CharField(max_length=6)
    jenisName = models.CharField(max_length=16)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.jenisName

# Tabel Pengguna
class Pengguna(models.Model):
    username = models.CharField(max_length=21, null=False)
    password = models.TextField(max_length=21, null=False)
    firstName = models.CharField(max_length=14, null=False)
    lastName = models.CharField(max_length=14, null=False)
    nik = models.TextField(max_length=60, blank=True)
    qr_code = models.IntegerField(null=False)
    time_login = models.IntegerField(default=5000)
    cookies    = models.TextField(max_length=21, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    department = models.ManyToManyField(Department, blank=True)
    divisi = models.ManyToManyField(Divisi, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return (f'{self.firstName} {self.lastName} - {self.department.all()[0]}')

    def get_department(self):
        if (self.department.count()==1):
            return self.department.all()[0]
        else:
            return self.department.all()[0]

# Table file
class File(models.Model):
    fileName = models.CharField(max_length=120)
    file = models.FileField(upload_to='', null=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.fileName
    
class Note(models.Model):
    user = models.ManyToManyField(Pengguna, related_name='note')
    note = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.note[:10] + '...'

# Tabel Berkas Masuk
class SuratMasuk(models.Model):
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    file = models.ManyToManyField(File, blank=True)
    fileName = models.CharField(max_length=40, default=file.name)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.CharField(choices=TYPE_BERKAS, max_length=10, default='B')
    # general purpose
    department = models.ManyToManyField(Department, blank=True)
    upload_for = models.ManyToManyField(Pengguna, related_name='target', blank=True)
    address_sender = models.CharField(max_length=160, null=True)
    sender = models.CharField(max_length=120, null=True)
    perihal = models.CharField(max_length=60)
    nomor_surat = models.CharField(max_length=60)
    created_at = models.CharField(null=True, max_length=10)
    url = models.CharField(null=True, max_length=40)
    ## Berkas workflow
    reader = models.ManyToManyField(Pengguna, related_name='reader', blank=True)
    approve_by = models.ManyToManyField(Pengguna, related_name='approved', blank=True)
    note = models.ManyToManyField(Note, blank=True)
    # status active/inactive file
    isArsip = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.fileName

# Tabel Berkas Masuk
class SuratKeluar(models.Model):
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    file = models.ManyToManyField(File, blank=True)
    fileName = models.CharField(max_length=120, default=file.name)
    jenisBerkas = models.ForeignKey(JenisBerkas, on_delete=models.CASCADE)
    typeBerkas = models.CharField(choices=TYPE_BERKAS, max_length=16,default='B')
    destination = models.CharField(max_length=160, null=True)
    destination_address = models.CharField(max_length=160, null=True)
    perihal = models.CharField(max_length=60)
    nomor_surat = models.CharField(max_length=60, null=True)
    created_at = models.CharField(null=True, max_length=10)
    url = models.CharField(null=True, max_length=40)
    status = models.BooleanField(default=True)
    isArsip = models.BooleanField(default=False)
    def __str__(self):
        return self.fileName

# Semua berkas yang sudah selesai
class Arsip(models.Model):
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    TYPE_GROUP = [('SM', 'Surat Masuk'), ('SK', 'Surat Keluar')]
    fileName = models.CharField(max_length=120)
    file_path = models.ManyToManyField(File, blank=True)
    perihal = models.CharField(max_length=60)
    nomor_surat = models.CharField(max_length=60, null=True)
    typeBerkas = models.CharField(choices=TYPE_BERKAS, max_length=16,default='B')
    group = models.CharField(choices=TYPE_GROUP, max_length=16,default='SM')
    created_at = models.CharField(null=True, max_length=10)
    status = models.BooleanField(default=True)
    url = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.fileName

