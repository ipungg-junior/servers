# Generated by Django 3.0.11 on 2021-09-22 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210921_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pengguna',
            name='department',
            field=models.ManyToManyField(blank=True, to='app.Department'),
        ),
    ]