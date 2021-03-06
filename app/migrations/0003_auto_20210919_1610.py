# Generated by Django 3.0.11 on 2021-09-19 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210917_0712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suratmasuk',
            name='signature',
        ),
        migrations.AlterField(
            model_name='suratmasuk',
            name='department',
            field=models.ManyToManyField(blank=True, to='app.Department'),
        ),
        migrations.AlterField(
            model_name='suratmasuk',
            name='upload_for',
            field=models.ManyToManyField(blank=True, related_name='target', to='app.Pengguna'),
        ),
    ]
