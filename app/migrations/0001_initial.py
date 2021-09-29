# Generated by Django 3.0.11 on 2021-09-17 06:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departementID', models.CharField(max_length=6)),
                ('departementName', models.CharField(max_length=21)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=40, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Divisi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('divisiID', models.CharField(max_length=6)),
                ('divisiName', models.CharField(max_length=21)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=40, null=True)),
                ('status', models.BooleanField(default=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Department')),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=120)),
                ('file', models.FileField(upload_to='')),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='JenisBerkas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenisCode', models.CharField(max_length=6)),
                ('jenisName', models.CharField(max_length=16)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pengguna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=21)),
                ('password', models.TextField(max_length=21)),
                ('firstName', models.CharField(max_length=14)),
                ('lastName', models.CharField(max_length=14)),
                ('nik', models.TextField(blank=True, max_length=60)),
                ('qr_code', models.IntegerField()),
                ('time_login', models.IntegerField(default=5000)),
                ('cookies', models.TextField(blank=True, max_length=21)),
                ('status', models.BooleanField(default=True)),
                ('department', models.ManyToManyField(to='app.Department')),
                ('divisi', models.ManyToManyField(to='app.Divisi')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roleCode', models.CharField(max_length=4)),
                ('roleName', models.CharField(max_length=16)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuratMasuk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(default=None, max_length=40)),
                ('typeBerkas', models.CharField(choices=[('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')], default='B', max_length=10)),
                ('address_sender', models.CharField(max_length=160, null=True)),
                ('sender', models.CharField(max_length=120, null=True)),
                ('perihal', models.CharField(max_length=60)),
                ('nomor_surat', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=40, null=True)),
                ('status', models.BooleanField(default=True)),
                ('approve_by', models.ManyToManyField(blank=True, related_name='approved', to='app.Pengguna')),
                ('department', models.ManyToManyField(to='app.Department')),
                ('file', models.ManyToManyField(to='app.File')),
                ('jenisBerkas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.JenisBerkas')),
                ('reader', models.ManyToManyField(blank=True, related_name='reader', to='app.Pengguna')),
                ('signature', models.ManyToManyField(blank=True, related_name='signature', to='app.Pengguna')),
                ('upload_for', models.ManyToManyField(related_name='target', to='app.Pengguna')),
            ],
        ),
        migrations.CreateModel(
            name='SuratKeluar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(default=None, max_length=120)),
                ('typeBerkas', models.CharField(choices=[('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')], default='B', max_length=16)),
                ('destination', models.CharField(max_length=160, null=True)),
                ('destination_address', models.CharField(max_length=160, null=True)),
                ('perihal', models.CharField(max_length=60)),
                ('nomor_surat', models.CharField(max_length=60, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(max_length=40, null=True)),
                ('department', models.ManyToManyField(to='app.Department')),
                ('file', models.ManyToManyField(to='app.File')),
                ('jenisBerkas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.JenisBerkas')),
            ],
        ),
        migrations.AddField(
            model_name='pengguna',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Role'),
        ),
        migrations.CreateModel(
            name='Arsip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileName', models.CharField(max_length=120)),
                ('perihal', models.CharField(max_length=60)),
                ('nomor_surat', models.CharField(max_length=60, null=True)),
                ('typeBerkas', models.CharField(choices=[('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')], default='B', max_length=16)),
                ('group', models.CharField(choices=[('SM', 'Surat Masuk'), ('SK', 'Surat Keluar')], default='SM', max_length=16)),
                ('file_path', models.ManyToManyField(to='app.File')),
            ],
        ),
    ]
