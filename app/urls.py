from django.urls import path, include
from .views import *


urlpatterns = [
    #root user
    path('super/', rootSuper),
    path('super/homepage/', rootHomepage, name='super-homepage'),
    path('super/detail/', rootDetail),
    path('super/homepage/department/', rootDepartment),
    path('super/homepage/suratmasuk/', rootSuratmasuk),
    path('super/homepage/suratkeluar/', rootSuratkeluar),
    path('super/homepage/arsip/', rootArsip),
    path('super/view/arsip/<str:ar>', rootArsipDetail),
    path('super/homepage/department/<str:divisi>', rootDivisi),
    path('super/homepage/user/', rootUser, name='super_user'),
    path('super/report/suratmasuk/', rootReportMasuk),
    path('super/report/suratkeluar/', rootReportKeluar),
    path('super/search/suratmasuk/', rootSearchMasuk),
    path('super/search/arsip/', rootSearchArsip),
    path('super/search/suratkeluar/', rootSearchKeluar),
    path('super/edit/suratmasuk/<str:fa>', rootEditSuratMasuk),
    path('super/edit/suratkeluar/<str:fa>', rootEditSuratKeluar),
    path('super/edit/user/<str:nm>', rootEditUser, name='superedituser'),
    path('super/register/department/', rootDepartmentRegister),
    path('super/register/divisi/<str:dpr>', rootDivisiRegister),
    path('super/homepage/user/register/', rootUserRegister),
    path('super/logout/', rootLogout),

    ## general purpose
    path('', login),
    path('login/', login),
    path('homepage/', homepage, name='homepage'),
    # url surat masuk   
    path('homepage/suratmasuk/', suratmasuk, name='suratmasuk'),
    path('homepage/suratmasuk/<str:filename>', suratmasukdetail, name='suratmasukdetail'),
    # url surat keluar
    path('homepage/suratkeluar/', suratkeluar, name='suratkeluar'),
    path('homepage/suratkeluar/<str:filename>', suratkeluardetail, name='suratkeluardetail'),
    path('homepage/suratberedar/', suratberedar, name='suratberedar'),
    path('homepage/arsip/', arsip, name='arsip'),
    path('homepage/arsip/detail/<str:x>', arsipDetail, name='arsipdetail'),
    path('homepage/download/<str:f>', download, name='downloadFile'),
    path('homepage/search/arsip/', searchArsip),
    path('approve/<str:file>', approve, name='approving'),
    path('delete/<str:fl>', delete),
    path('delete/arsip/<str:fs>', deleteArsip),
    path('delete/department/<str:dptmn>', deleteDepartment),
    path('delete/divisi/<str:dvi>', deleteDivisi),
    path('uplink/<str:us>', uplink),
    path('downlink/<str:us>', downlink),
    path('logout/', logout, name='logout')
]

