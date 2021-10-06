from django import forms
from django.db.models import query
from django.forms import fields
from django.forms import widgets
from django.forms.widgets import Widget
from django.http import request
from .models import *
import datetime

class UploadFileForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'class':'form-control', 'required': 'False'}))


class FormSuratMasuk(forms.Form):
    datenow = datetime.date.today().strftime('%d/%m/%Y')
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    fileName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    perihal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nomor_surat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address_sender = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sender = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    typeBerkas = forms.ChoiceField(choices=TYPE_BERKAS, widget=forms.Select(attrs={'class': 'custom-select'}))
    jenisBerkas = forms.ModelChoiceField(queryset=JenisBerkas.objects.all(), to_field_name="jenisName", widget=forms.Select(attrs={'class': 'custom-select'}))
    upload_for = forms.ModelMultipleChoiceField(queryset=Pengguna.objects.all().filter(status=True), to_field_name="username", widget=forms.SelectMultiple(attrs={'class': 'custom-select'}))
    created_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': datenow}))
    
class FormSuratKeluar(forms.Form):
    datenow = datetime.date.today().strftime('%d/%m/%Y')
    TYPE_BERKAS = [('B', 'Biasa'), ('P', 'Penting'), ('SP', 'Sangat Penting')]
    fileName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    perihal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nomor_surat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    des = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    typeBerkas = forms.ChoiceField(choices=TYPE_BERKAS, widget=forms.Select(attrs={'class': 'custom-select'}))
    jenisBerkas = forms.ModelChoiceField(queryset=JenisBerkas.objects.all(), to_field_name="jenisName", widget=forms.Select(attrs={'class': 'custom-select'}))
    created_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': datenow}))
    
class SearchSurat(forms.Form):
    suratmasuk = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Cari Surat Masuk'}))
    suratkeluar = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Cari Surat Keluar'}))
    arsip = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Cari Arsip'}))
    judul = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Judul'}))
    date = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Tanggal'}))
    bulan = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Bulan'}))
    perihal = forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'inlineFormInputGroup2', 'placeholder': 'Perihal'}))

class PenggunaRegister(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'password'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    firstName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nik = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ModelChoiceField(queryset=Role.objects.all(), to_field_name="roleName", widget=forms.Select(attrs={'class': 'custom-select'}))
    department = forms.ModelMultipleChoiceField(queryset=Department.objects.all(), to_field_name="departementID", widget=forms.SelectMultiple(attrs={'class': 'custom-select'}))
    divisi = forms.ModelChoiceField(queryset=Divisi.objects.all(), to_field_name="divisiID", widget=forms.Select(attrs={'class': 'custom-select', 'required': 'False'}))

class PenggunaEdit(forms.ModelForm):
    class Meta:
        model = Pengguna
        fields = ['username', 'password', 'firstName', 'lastName', 'nik', 'department', 'divisi']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            'firstName': forms.TextInput(attrs={'class': 'form-control'}),
            'lastName': forms.TextInput(attrs={'class': 'form-control'}),
            'nik': forms.TextInput(attrs={'class': 'form-control'}),
        }

    department = forms.ModelMultipleChoiceField(queryset=Department.objects.all(), to_field_name="departementID", widget=forms.SelectMultiple(attrs={'class': 'custom-select'}))
    divisi = forms.ModelChoiceField(queryset=Divisi.objects.all(), to_field_name='divisiID', widget=forms.Select(attrs={'class': 'custom-select'}))

class FormNote(forms.Form):
    note = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tambahkan catatan...', 'required': False}))



class FormDepartmentDivisi(forms.Form):
    departmentID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MAX 3 huruf'}))
    departmentName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    divisiID = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MAX 3 huruf'}))
    divisiName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
