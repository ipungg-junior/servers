# Generated by Django 3.0.11 on 2021-09-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210922_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='arsip',
            name='url',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=120, null=True)),
                ('user', models.ManyToManyField(blank=True, to='app.Pengguna')),
            ],
        ),
        migrations.AddField(
            model_name='suratmasuk',
            name='note',
            field=models.ManyToManyField(blank=True, to='app.Note'),
        ),
    ]
