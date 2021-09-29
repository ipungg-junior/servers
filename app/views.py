from django.http import response
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, HttpResponseServerError, JsonResponse, FileResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from .supervisor import Supervisor
import random, string, datetime
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import xlwt


supervisor = Supervisor()

def rand():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(17))

def download(request, f):
    li = []
    fl = File.objects.get(file=f)
    file_handle = fl.file.open()
    response = FileResponse(file_handle, content_type='application/pdf')
    response['Content-Length'] = fl.file.size
    response['Content-Disposition'] = 'attachment; filename="%s"' % fl.file.name
    return response


def login(request):
    if (request.method=='GET'):
        try:
            reqCookie = request.COOKIES['auth']
            user = Pengguna.objects.get(cookies=reqCookie)
            if (user.status):
                return redirect('/homepage')
            else:
                return render(request, 'user/login.html')
        except:
            return render(request, 'user/login.html')
    else:
        try:
            reqUsername = request.POST['username']
            reqPassword = request.POST['katasandi']

            user = Pengguna.objects.get(username=reqUsername)
            if (reqPassword==user.password):
                if (user.status):
                    response = redirect(f'/homepage')
                    user.cookies = rand()
                    user.save()
                    response.set_cookie('auth', user.cookies, max_age=10000)
                    return response
                else:
                    return redirect('/homepage')
            else:
                return redirect('/homepage')
        except:
            # eror data eror
            return redirect('/homepage')

def logout(request):
    resp = redirect('/login')
    resp.delete_cookie('auth')
    return resp

def homepage(request):
    status = False
    try:
        cookies = request.COOKIES['auth']
        user = Pengguna.objects.get(cookies=cookies)
        status = True
    except:
        status = False
    if (status):
        sm_list = supervisor.getSuratMasukfor(user)
        unapprove = supervisor.checkApproving(sm_list, user)
        sk_list = SuratKeluar.objects.all().filter(status=True)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)
        arsip = Arsip.objects.all().filter(status=True)
        return render(request, 'user/homepage.html', context={
            'user': user,
            'notifications_list': notification_list,
            'unapprove': unapprove,
            'arsip': arsip,
            'sm_list': sm_list,
            'sk_list': sk_list})
    else:
        return redirect('/login')

def suratberedar(request):
    status, user = supervisor.authenticate(request)
    if (status):
        sm_list = supervisor.getSuratMasukfor(user)
        unapprove = supervisor.checkApproving(sm_list, user)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)

        return render(request, 'user/suratberedar.html', context={
            'user': user,
            'unapprove': unapprove,
            'notifications_list': notification_list,
            'sm_list': sm_list})
    else:
        return redirect('/login')

def suratmasuk(request):
    status, user = supervisor.authenticate(request)
    if (status):
        sm_list = supervisor.getSuratMasukfor(user)
        unapprove = supervisor.checkApproving(sm_list, user)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)

        return render(request, 'user/suratmasuk.html', context={
            'user': user,
            'notifications_list': notification_list,
            'sm_list': sm_list})
    else:
        return redirect('/login')

def suratkeluar(request):
    status = False
    try:
        cookie = request.COOKIES['auth']
        user = Pengguna.objects.get(cookies=cookie)
        status = True
    except:
        return redirect('/login')
    if(status):
        sk_list = SuratKeluar.objects.all().filter(status=True).order_by('-created_at')
        notifications_list = supervisor.getSuratMasukNotifications(user)
        page = request.GET.get('page', 1)
        paginator = Paginator(sk_list, 15)
        try:
            arsip_filter = paginator.page(page)
        except PageNotAnInteger:
            arsip_filter = paginator.page(1)
        except EmptyPage:
            arsip_filter = paginator.page(paginator.num_pages)
        return render(request, 'user/suratkeluar.html', context={
            'user': user,
            'notifications_list': notifications_list,
            'sk_list': arsip_filter
        })

@xframe_options_exempt
def suratmasukdetail(request, filename):
    status, user = supervisor.authenticate(request)
    if (status):
        ## ambil file dan save reader
        file_list = File.objects.filter(fileName=filename)
        suratmasuk = supervisor.getSuratMasukByUrl(filename)
        suratmasuk.reader.add(user)
        suratmasuk.save()
        approve_by = suratmasuk.approve_by.all()
        reader = suratmasuk.reader.all()
        state = False
        for i in approve_by:
            if (i.username == user.username):
                state = True

        # Ambil catatan berkas
        note = suratmasuk.note.all()
        form_note = FormNote()
        return render(request, 'user/suratmasukdetail.html', context={
            'user' : user,
            'file': file_list,
            'reader_list': reader,
            'approve_list': approve_by,
            'surat': suratmasuk,
            'selfApprove': state,
            'note_list': note,
            'form_note': form_note
        })
    else:
        return redirect('/login')

def suratkeluardetail(request, filename):
    status, user = supervisor.authenticate(request)
    if (status):
        ## ambil file dan save reader
        file = supervisor.getFile(filename)
        return render(request, 'user/suratkeluardetail.html', context={
            'user' : user,
            'file': file,
        })
    else:
        return redirect('/login')

def arsip(request):
    status, user = supervisor.authenticate(request)
    if (status):
        arsip_list = Arsip.objects.all().filter(status=True).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(arsip_list, 15)
        ## Notification
        notification_list = supervisor.getSuratMasukNotifications(user)
        try:
            arsip_filter = paginator.page(page)
        except PageNotAnInteger:
            arsip_filter = paginator.page(1)
        except EmptyPage:
            arsip_filter = paginator.page(paginator.num_pages)

        form_search = SearchSurat()
        return render(request, 'user/arsip.html', context={
            'user': user,
            'notifications_list': notification_list,
            'arsip': arsip_filter,
            'form_search': form_search})
    else:
        return redirect('/login')

@csrf_exempt
def searchArsip(request):
    user = Pengguna.objects.get(cookies=request.COOKIES['auth'])
    list_surat = []
    if (request.method=='POST'):
        form = SearchSurat(request.POST)
        keyword = str(form['arsip'].value()).upper()
        arsip_list = Arsip.objects.all().order_by('-created_at')
        notif = supervisor.getSuratMasukNotifications(user)
        # search by name
        try:

            # Search by date
            if (str(keyword[0:7])=='TANGGAL'):
                for l in arsip_list:
                    if(str(l.created_at[1])=='/'):
                        if(str(l.created_at[0:1])==keyword[8:]):
                            list_surat.append(l)
                    if(str(l.created_at[0:2])==keyword[8:]):
                        list_surat.append(l)
                return render(request, 'user/searcharsip.html', context={
                    'user': user,
                    'arsip': list_surat,
                    'notifications_list': notif,
                    'title': 'Arsip'
                })

                # Search by date
            if (str(keyword[0:5])=='BULAN'):
                for l in arsip_list:
                    if(str(l.created_at[1])=='/'):
                        if(str(l.created_at[2:4])==keyword[6:]):
                            list_surat.append(l)
                    if(str(l.created_at[3:5])==keyword[6:]):
                        list_surat.append(l)
                return render(request, 'user/searcharsip.html', context={
                    'user': user,
                    'arsip': list_surat,
                    'notifications_list': notif,
                    'title': 'Arsip'
                })

            for d in arsip_list:
                if(str(d.fileName).__contains__(keyword)):
                    list_surat.append(d)
            for x in arsip_list:
                if(str(x.nomor_surat).__contains__(keyword)):
                    list_surat.append(x)
            return render(request, 'user/searcharsip.html', context={
                'user': user,
                'arsip': list_surat,
                'notifications_list': notif,
                'title': 'Arsip'
            })
                 
        except:
            return JsonResponse({'status': '500 Internal Server Error'})

    else:
        pass

def arsipDetail(request, x):
    status, user = supervisor.authenticate(request)
    if (status):
        ## ambil file dan save reader
        file_list = File.objects.filter(fileName=x)
        arsip = Arsip.objects.get(url=x)
        if arsip.group == 'SM':
            berkas = SuratMasuk.objects.filter(url=x)
            note_list = berkas[0].note.all()

            return render(request, 'user/arsipdetail.html', context={
                'user' : user,
                'file': file_list,
                'surat': berkas[0],
                'note_list': note_list
            })
        else:
            berkas = SuratKeluar.objects.get(url=x)
            return render(request, 'user/arsipdetailkeluar.html', context={
                'user' : user,
                'file': file_list,
                'surat': berkas,
            })
    else:
        return redirect('/login')

def approve(request, file):
    cookies = request.COOKIES['auth']
    if request.method=='POST':
        form_note = FormNote(request.POST)
        try:
            user = Pengguna.objects.get(cookies=cookies)
            berkas = SuratMasuk.objects.get(url=file)
            if str(form_note['note'].value()) == '':
                pass
            else:
                note = Note(note=str(form_note['note'].value()))
                note.save()
                note.user.add(user)
                berkas.note.add(note)
            berkas.approve_by.add(user)
            berkas.save()

            fl = File.objects.filter(fileName=berkas.url)
            print(fl)
            total_target = berkas.upload_for.all().count()
            total_approve = berkas.approve_by.all().count()
            print(total_target)
            print(total_approve)
            if (total_target==total_approve):
                try:
                    ar = Arsip.objects.get(fileName=berkas.fileName)
                    return redirect('/homepage')
                except:
                    arsip = Arsip(
                        fileName=berkas.fileName,
                        perihal=berkas.perihal,
                        nomor_surat=berkas.nomor_surat,
                        typeBerkas=berkas.typeBerkas,
                        group='SM',
                        url=berkas.url,
                        created_at=(datetime.date.today().strftime('%d/%m/%Y')),
                    )
                    arsip.save()
                    print('berhasil buat objek arsip')
                    for i in fl:
                        arsip.file_path.add(i)
                        arsip.save()
                    berkas.isArsip = True
                    berkas.save()
                    print('berhasil save')
                    return redirect('/homepage/')
                
            else:
                return redirect('/homepage/')
        except:
            return redirect('/homepage/')

@csrf_exempt
def delete(request, fl):
    print(fl)
    status = supervisor.delete(fl)
    return redirect('/super/homepage')

def deleteArsip(request, fs):
    status = supervisor.deleteArsip(fs)
    return redirect('/super/homepage')

@csrf_exempt
def uplink(request, us):
    usr = Pengguna.objects.get(username=us)
    usr.status = True
    usr.save()
    return redirect('/super/homepage/user')

@csrf_exempt
def downlink(request, us):
    usr = Pengguna.objects.get(username=us)
    usr.status = False
    usr.save()
    return redirect('/super/homepage/user')

@csrf_exempt
def deleteDepartment(request, dptmn):
    dprtmn = Department.objects.get(departementID=dptmn)
    # dprtmn.status = False
    # dprtmn.save()
    default_divisi = Divisi.objects.get(divisiID='DFLT')
    default_department = Department.objects.get(departementID='DLT')
    included_divisi = dprtmn.divisi_set.all().count()
        ## Tidak ada divisi didalamnya
    if (included_divisi==0):
        user_list = dprtmn.pengguna_set.all()
        if (user_list.count()==0):
            dprtmn.delete()
        else:
            for i in user_list:
                i.department.add(default_department)
                i.department.remove(dprtmn)
            dprtmn.delete()
    
    ## Ada divisi didalamnya
    else:
        divisi_list = dprtmn.divisi_set.all()
        for i in divisi_list:
            user_list = i.pengguna_set.all()    # Ambil pengguna dalam divisi
            if (user_list.count()==0):
                i.delete()
            else:
                for user in user_list:          # Ambil user di divisi
                    current_divisi = user.divisi.all()[0]
                    current_department = user.department.all()[0]
                    user.divisi.remove(current_divisi)
                    user.divisi.add(default_divisi)
                    user.department.add(default_department)
                    user.department.remove(current_department)
                i.delete()
        dprtmn.delete()
    return redirect('/super/homepage/department')

    
@csrf_exempt
def deleteDivisi(request, dvi):
    divisi = Divisi.objects.get(divisiID=dvi)
    default_divisi = Divisi.objects.get(divisiID='DFLT')
    user_list = divisi.pengguna_set.all()    # Ambil pengguna dalam divisi
    if (user_list.count()==0):
        divisi.delete()
    else:
        for user in user_list:          # Ambil user di divisi
            user.divisi.remove(divisi)
            user.divisi.add(default_divisi)
        divisi.delete()
    return redirect('/super/homepage/department')
  
    
####
####    ROOT BACKEND
####

def rootSuper(request):

    if request.method == 'POST':
        if (request.POST['passcode']=='55555'):
            response = redirect('/super/homepage')
            response.set_cookie('master', 55555, max_age=8000)
            return response
        else:
            return redirect('/super/')
    else:
        resp = render(request, 'super/super.html')
        resp.delete_cookie('auth')
        return resp      

def rootHomepage(request):
    search = SearchSurat()
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            if (request.method=='GET'):
                try:
                    sm_list = SuratMasuk.objects.filter(status=True).order_by('-created_at')
                    unapprove_list = []
                    for i in sm_list:
                        if (i.upload_for.all().count() == i.approve_by.all().count()):
                            pass
                        else:
                            unapprove_list.append(i)
                    arsip = Arsip.objects.all().filter(status=True)         
                    sk_list = SuratKeluar.objects.all()
                    reminder = False
                    date = str(datetime.date.today().strftime('%d'))
                    if date=='29':
                        reminder = True
                    if date=='30':
                        reminder = True
                    month = datetime.date.today().strftime('%B')
                    return render(request, 'super/super_homepage.html', context={
                        'unapprove_count': len(unapprove_list),
                        'arsip': arsip,
                        'sb_list': unapprove_list,
                        'sm_list': sm_list,
                        'sk_list': sk_list,
                        'form_search': search,
                        'month': month,
                        'reminder': reminder,
                    })
                except:
                    print('EROR SAAT MENGAMBIL DATA SUPER')
            return render(request, 'super/super_homepage.html', context={})
    except:
        return redirect('/super/')

@csrf_exempt
def rootSearchMasuk(request):
    list_surat = []
    if (request.method=='POST'):
        form = SearchSurat(request.POST)
        suratmasuk = str(form['suratmasuk'].value()).upper()
        data_list = SuratMasuk.objects.all().filter(status=True)
        # search by name
        try:
            for d in data_list:
                if(str(d.fileName).__contains__(suratmasuk)):
                    list_surat.append(d)
        except:
            pass
        #search by pengirim
        try:
            for d in data_list:
                if(str(d.sender).__contains__(suratmasuk)):
                    for i in list_surat:
                        if i==d:
                            pass
                        else:
                            list_surat.append(d)
        except:
            pass
        #search by perihal
        try:
            for d in data_list:
                if(str(d.perihal).__contains__(suratmasuk)):
                    for i in list_surat:
                        if i==d:
                            pass
                        else:
                            list_surat.append(d)
        except:
            pass

        return render(request, 'super/super_search.html', context={
            's_list': list_surat,
            'title': 'Surat Masuk'
        })

@csrf_exempt
def rootSearchKeluar(request):
    list_surat = []
    if (request.method=='POST'):
        form = SearchSurat(request.POST)
        suratkeluar = str(form['suratkeluar'].value()).upper()
        data_list = SuratKeluar.objects.all().filter(status=True)
        # search by name
        try:
            for d in data_list:
                if(str(d.fileName).__contains__(suratkeluar)):
                    list_surat.append(d)
        except:
            pass
        #search by pengirim
        try:
            for d in data_list:
                if(str(d.sender).__contains__(suratkeluar)):
                    for i in list_surat:
                        if i==d:
                            pass
                        else:
                            list_surat.append(d)
        except:
            pass
        #search by perihal
        try:
            for d in data_list:
                if(str(d.perihal).__contains__(suratkeluar)):
                    for i in list_surat:
                        if i==d:
                            pass
                        else:
                            list_surat.append(d)
        except:
            pass

        return render(request, 'super/super_search.html', context={
            's_list': list_surat,
            'title': 'Surat Keluar'
        })
            
@csrf_exempt
def rootSuratmasuk(request):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            form_file = UploadFileForm()
            form_berkas = FormSuratMasuk()
            if (request.method=='GET'):
                try:
                    return render(request, 'super/super_inputmasuk.html', context={
                        'form_file' : form_file,
                        'form_berkas': form_berkas,
                        })
                except:
                    print('EROR SAAT MENGAMBIL DATA SUPER')
            else:
                form = UploadFileForm(request.POST, request.FILES)
                form_berkas = FormSuratMasuk(request.POST)
                files = request.FILES.getlist('files')
                # Buat variable
                try:
                    status = supervisor.addSuratMasuk(files, form_berkas)
                except:
                    return HttpResponseServerError()
                return redirect('/super/homepage/')
    except:
        return redirect('/super/')

@csrf_exempt
def rootSearchArsip(request):
    list_surat = []
    if (request.method=='POST'):
        form = SearchSurat(request.POST)
        arsip_list = Arsip.objects.all()
        judul = str(form['arsip'].value()).upper()
        date = str(form['date'].value()).upper()
        month = str(form['bulan'].value()).upper()
        perihal = str(form['perihal'].value()).upper()
        by_judul = False
        by_date = False
        by_month = False
        by_perihal = False

        if judul!='':
            by_judul = True
        if date!='':
            by_date = True
        if month!='':
            by_month = True
        if perihal!='':
            by_perihal = True

        if by_month:
            if by_date:
                if by_perihal:
                    print('here')
                    for l in arsip_list:
                        if(str(l.created_at[1])=='/'):
                            if(str(l.created_at[2:4])==month):
                                list_surat.append(l)
                        if(str(l.created_at[3:5])==month):
                            list_surat.append(l)
                    return render(request, 'super/super_search.html', context={
                        'list_arsip': list_surat,
                        'title': 'Arsip'
                    })
                else:
                    pass
            else:
                if perihal:
                    pass
                else:
                    pass

        else:
            if date:
                if perihal:
                    pass
                else:
                    pass

            else:
                if perihal:
                    pass
                else:
                    pass

#        Search by date
#        # if (str(keyword[0:7])=='TANGGAL'):
#            # for l in arsip_list:
#                # if(str(l.created_at[1])=='/'):
#                    # if(str(l.created_at[0:1])==keyword[8:]):
#                        # list_surat.append(l)
#                # if(str(l.created_at[0:2])==keyword[8:]):
#                    # list_surat.append(l)
#            # return render(request, 'super/super_search.html', context={
#                # 'list_arsip': list_surat,
#                # 'title': 'Arsip'
#            # })
# #
#            Search by date
#        # if (str(keyword[0:5])=='BULAN'):
#            # for l in arsip_list:
#                # if(str(l.created_at[1])=='/'):
#                    # if(str(l.created_at[2:4])==keyword[6:]):
#                        # list_surat.append(l)
#                # if(str(l.created_at[3:5])==keyword[6:]):
#                    # list_surat.append(l)
#            # return render(request, 'super/super_search.html', context={
#                # 'list_arsip': list_surat,
#                # 'title': 'Arsip'
#            # })
# #
#        # if by_judul:
#            # for d in arsip_list:
#                # if(str(d.fileName).__contains__(keyword)):
#                    # list_surat.append(d)
#        # 
#        Search by nomor surat
#        # for x in arsip_list:
#            # if(str(x.nomor_surat).__contains__(keyword)):
#                # list_surat.append(x)
# #
#        # return render(request, 'super/super_search.html', context={
#            # 'list_arsip': list_surat,
#            # 'title': 'Arsip'
#        # })
    
    else:
        return JsonResponse({
            'status': '403',
            'info': 'Access Denied for \'GET\' Method',
        })

def rootArsip(request):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            arsip_list = Arsip.objects.all().filter(status=True).order_by('-created_at')
            page = request.GET.get('page', 1)
            paginator = Paginator(arsip_list, 15)
            try:
                arsip_filter = paginator.page(page)
            except PageNotAnInteger:
                arsip_filter = paginator.page(1)
            except EmptyPage:
                arsip_filter = paginator.page(paginator.num_pages)
            form_arsip = SearchSurat()
            return render(request, 'super/super_arsip.html', context={
                'form_search': form_arsip,
                'arsip': arsip_filter
            })
    except:
        return redirect('/super/')

@csrf_exempt
def rootArsipDetail(request, ar):
    try:
        surat = SuratMasuk.objects.get(url=ar)
        file = File.objects.filter(fileName=ar)
        return render(request, 'super/super_arsipmasukdetail.html', context={
            'file': file,
            'surat': surat
        })
    except:
        surat = SuratKeluar.objects.get(url=ar)
        file = File.objects.filter(fileName=ar)
        return render(request, 'super/super_arsipkeluardetail.html', context={
            'file': file,
            'surat': surat
        })

@csrf_exempt
def rootSuratkeluar(request):
    base_form_file = UploadFileForm()
    base_form_berkas = FormSuratKeluar()
    if (request.method=='GET'):
        try:
            return render(request, 'super/super_inputkeluar.html', context={
                'form_file' : base_form_file,
                'form_berkas': base_form_berkas})
        except:
            print('EROR SAAT MENGAMBIL DATA SUPER')
    else:
        form = UploadFileForm(request.POST, request.FILES)
        form_berkas = FormSuratKeluar(request.POST)
        files = request.FILES.getlist('files')
        # Buat variable
        try:
            status = supervisor.addSuratKeluar(files, form_berkas)
        except:
            print('error')
        return redirect('/super/homepage')

@csrf_exempt
def rootEditSuratMasuk(request, fa):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            surat = SuratMasuk.objects.get(url=fa)
            file_s = File.objects.filter(fileName=fa)
            if (request.method=='POST'):
                form_edit = FormSuratMasuk(request.POST)

                try:
                    files = request.FILES.getlist('files')
                    addUser = form_edit['upload_for'].value()
                except:
                    print('EROR FILES')

                if len(files)==0:
                    # cuman tambah user
                    for i in addUser:
                        obj = Pengguna.objects.get(username=i)
                        surat.upload_for.add(obj)
                        surat.save()
                else:
                    for i in files:
                        obj = File(fileName=fa, file=i)
                        obj.save()
    except:
        return redirect('/super/')

    else:
        form_edit_get = FormSuratMasuk()
        form_file = UploadFileForm()
        return render(request, 'super/super_detailsuratmasuk.html', context={
            'surat': surat,
            'file': file_s,
            'form_edit': form_edit_get,
            'form_file': form_file
        })

@csrf_exempt
def rootEditSuratKeluar(request, fa):
    surat = SuratKeluar.objects.get(url=fa)
    file_s = File.objects.get(fileName=fa)
    if (request.method=='POST'):
        return render(request, 'super/super_detailsuratkeluar.html', context={
            'surat': surat,
            'file': file_s
        })

def rootaddUpload(request):
    if (request.method=='POST'):
        form = FormSuratMasuk(request.POST)
        print(form['upload_for'].value())
        return redirect('/super/homepage/')

def rootDepartment(request):
    dep_list = Department.objects.all().filter(status=True)
    return render(request, 'super/super_department.html', context={
        'd_list': dep_list,
    })

def rootDivisi(request, divisi):
    d_obj = Department.objects.get(url=divisi)
    div_list = Divisi.objects.filter(department=d_obj).filter(status=True)
    return render(request, 'super/super_divisi.html', context={
        'divisi_list': div_list,
        'd_obj': d_obj
    })

def rootUser(request):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            user_list = Pengguna.objects.all().filter(status=True)
            user_deactivate = Pengguna.objects.all().filter(status=False)
            return render(request, 'super/super_user.html', context={
                'user_list': user_list,
                'user_deactivate': user_deactivate
            })
    except:
        return redirect('/super/')

def rootUserRegister(request):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            if (request.method=='GET'):
                form_register = PenggunaRegister()
                return render(request, 'super/super_userregister.html', context={
                    'form_register': form_register
                })
            else:
                # Get all value and create new obj Pengguna
                form_register = PenggunaRegister(request.POST)
                if (str(form_register['password'].value())==str(form_register['password1'].value())):
                    status, msg = supervisor.addPengguna(form_register)
                    if status:
                        return redirect('/super/homepage/user')
                    else:
                        return JsonResponse({
                        'info': msg
                    })
                else:
                    return JsonResponse({
                        'info': 'password tidak cocok'
                    })
    except:
        return redirect('/super/')

@csrf_exempt
def rootEditUser(request, nm):

    user = Pengguna.objects.get(username=nm)
    if request.method == 'POST':
        form = PenggunaEdit(request.POST)
        user.username = str(form['username'].value())
        user.password = str(form['password'].value())
        user.firstName = str(form['firstName'].value())
        user.lastName = str(form['lastName'].value())
        user.nik = str(form['nik'].value())
        department = form['department'].value()[0]
        divisi = str(form['divisi'].value())
        default_department = Department.objects.get(departementID='DLT')
        default_divisi = Divisi.objects.get(divisiID='DFLT')
        department_changes = Department.objects.get(departementID=department)
        divisi_changes = Divisi.objects.get(divisiID=divisi)


        print(department)
        print(divisi)

        if department=='DLT':
            current_dp = user.department.all()[0]
            current_dv = user.divisi.all()[0]
            user.department.remove(current_dp)
            user.department.add(default_department)
            user.divisi.remove(current_dv)
            user.divisi.add(default_divisi)
            return redirect('/super/homepage/user')

        if divisi=='DFLT':
            current_dp = user.department.all()[0]
            current_dv = user.divisi.all()[0]
            user.department.remove(current_dp)
            user.department.add(department_changes)
            user.divisi.remove(current_dv)
            user.divisi.add(default_divisi)
            return redirect('/super/homepage/user')
        
        user.department.remove(default_department)
        user.department.add(department_changes)
        user.divisi.remove(default_divisi)
        user.divisi.add(divisi_changes)
        user.save()
        return redirect('/super/homepage/user')
    else:    
        form = PenggunaEdit(instance=user)
        return render(request, 'super/super_edituser.html', context={
            'user': user,
            'form': form
        })

def rootDepartmentRegister(request):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            if (request.method=='POST'):
                form = FormDepartmentDivisi(request.POST)
                dID = str(form['departmentID'].value())
                dName = str(form['departmentName'].value()).capitalize()
                try:
                    obj = Department(departementID=dID, departementName=dName)
                    obj.url = dName.replace(' ', '-').lower()
                    obj.save()
                except:
                    print('GAGAL MEMBUAT DEPARTMENT')

                return redirect('/super/homepage/department')
            else:
                form = FormDepartmentDivisi()
                return render(request, 'super/super_departmentregister.html', context={
                    'form': form
                })
    except:
        return redirect('/super/')


def rootDivisiRegister(request, dpr):
    try:
        cookie = request.COOKIES['master']
        if cookie=='55555':
            if (request.method=='POST'):
                dpr = Department.objects.get(url=dpr)
                form = FormDepartmentDivisi(request.POST)
                dID = str(form['divisiID'].value())
                dName = str(form['divisiName'].value()).capitalize()
                try:
                    obj = Divisi(divisiID=dID, divisiName=dName)
                    obj.url = dName.replace(' ', '-').lower()
                    obj.save()
                    obj.department = dpr
                    obj.save()
                except:
                    print('GAGAL MEMBUAT DIVISI')

                return redirect('/super/homepage/department')
            else:
                form = FormDepartmentDivisi()
                return render(request, 'super/super_divisiregister.html', context={
                    'form': form
                })
    except:
        return redirect('/super/')


@csrf_exempt
def rootReportMasuk(request):
    # Ambil bulan sekarang
    month = datetime.date.today().strftime('%m')
    year = datetime.date.today().strftime('%Y')
    # Ambil arsip surat masuk
    arsip_list = Arsip.objects.filter(group='SM').order_by('-created_at')
    report = []
    # cocokan bulan dan tahun di surat, jika cocok masuk list report
    for i in arsip_list:
        if (str(i.created_at[1])=='/'):
            if (str(i.created_at[2:4])==month and str(i.created_at[5:])==year):
                berkas = SuratMasuk.objects.get(url=i.url)
                report.append(berkas)
        if (str(i.created_at[3:5])==month and str(i.created_at[6:])==year):
            berkas = SuratMasuk.objects.get(url=i.url)
            report.append(berkas)

    if (request.method=='GET'):
        return render(request, 'super/super_reportmasuk.html', context={
            'month': str(datetime.date.today().strftime('%B')).lower(),
            'year': year,
            'total': len(report),
            'report_list': report
        })
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Laporan-surat-masuk-{month}-{year}.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Arsip')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['No','Judul Surat', 'Nomor Surat', 'Perihal', 'Pengirim', 'Tanggal']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        for row in report:
            row_num += 1
            for col_num in range(6):
                if col_num==0:
                    ws.write(row_num, col_num, row_num, font_style)
                if col_num==1:
                    ws.write(row_num, col_num, row.fileName, font_style)
                if col_num==2:
                    ws.write(row_num, col_num, row.nomor_surat, font_style)
                if col_num==3:
                    ws.write(row_num, col_num, row.perihal, font_style)
                if col_num==4:
                    ws.write(row_num, col_num, row.sender, font_style)
                if col_num==5:
                    ws.write(row_num, col_num, row.created_at, font_style)

        wb.save(response)
        return response

@csrf_exempt
def rootReportKeluar(request):
    # Ambil bulan sekarang
    month = datetime.date.today().strftime('%m')
    year = datetime.date.today().strftime('%Y')
    # Ambil arsip surat keluar
    arsip_list = Arsip.objects.filter(group='SK').order_by('-created_at')
    report = []
    # cocokan bulan dan tahun di surat, jika cocok masuk list report
    for i in arsip_list:
        if (str(i.created_at[1])=='/'):
            if (str(i.created_at[2:4])==month and str(i.created_at[5:])==year):
                berkas = SuratKeluar.objects.get(url=i.url)
                report.append(berkas)
        if (str(i.created_at[3:5])==month and str(i.created_at[6:])==year):
            berkas = SuratKeluar.objects.get(url=i.url)
            report.append(berkas)

    if (request.method=='GET'):
        return render(request, 'super/super_reportkeluar.html', context={
            'month': str(datetime.date.today().strftime('%B')).lower(),
            'year': year,
            'total': len(report),
            'report_list': report
        })
    else:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Laporan-surat-keluar-{month}-{year}.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Arsip')
        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['No', 'Judul Surat', 'Nomor Surat', 'Perihal', 'Penerima', 'Tanggal']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)
        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        for row in report:
            row_num += 1
            for col_num in range(6):
                if col_num==0:
                    ws.write(row_num, col_num, row_num, font_style)
                if col_num==1:
                    ws.write(row_num, col_num, row.fileName, font_style)
                if col_num==2:
                    ws.write(row_num, col_num, row.nomor_surat, font_style)
                if col_num==3:
                    ws.write(row_num, col_num, row.perihal, font_style)
                if col_num==4:
                    ws.write(row_num, col_num, row.destination, font_style)
                if col_num==5:
                    ws.write(row_num, col_num, row.created_at, font_style)

        wb.save(response)
        return response

def rootDetail(request):
    pass

def rootLogout(request):
    resp = redirect('/super')
    resp.delete_cookie('master')
    return resp
