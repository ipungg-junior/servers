# Generated by Django 3.0.11 on 2021-09-19 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210919_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suratmasuk',
            name='file',
            field=models.ManyToManyField(blank=True, to='app.File'),
        ),
    ]
