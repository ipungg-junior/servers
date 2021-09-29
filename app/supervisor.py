import os, random, string
from .models import *
import datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Supervisor():

    def __init__(self):
        pass

    def rand8(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))

    def randNum(self):
        return ''.join(random.choice(string.digits) for i in range(4))

    # Create 'MEDIA' directory, return false if already exist
    def authenticate(self, request):
        ## Auth with cookie
        if (request.method=='GET'):
            try:
                reqCookie = request.COOKIES['auth']
                user = Pengguna.objects.get(cookies=reqCookie)
                if (user.status):
                    return (True, user)
                else:
                    return (False, None)
            except:
                return (False, None)

        ## auth with login
        if (request.method=='POST'):
            reqUsername = request.POST['namapengguna']
            reqPassword = request.POST['katasandi']
            try:
                user = Pengguna.objects.get(username=reqUsername)
                if (reqPassword==user.password):
                    if (user.status):
                        return (True, user)
                    else:
                        return (False, None)
                else:
                    return (False, None)
            except:
                return (False, None)

    def getDepartment(self, url):
        d_obj = Department.objects.get(url=url)
        return d_obj

    def getAllDepartment(self):
        d_obj = Department.objects.all()
        return d_obj

    def getAllSuratMasuk(self):
        s_list = SuratMasuk.objects.all()
        return s_list

    def getAllSuratMasukActive(self):
        s_list = SuratMasuk.objects.filter(status=True).order_by('-created-at')
        return s_list
        
    def getAllSuratKeluarActive(self):
        s_list = SuratKeluar.objects.filter(status=True).order_by('-created-at')
        return s_list

    def getSuratMasukfor(self, user):
        s_list = SuratMasuk.objects.filter(upload_for=user).filter(status=True).filter(isArsip=False)
        return s_list

    def getSuratMasukNotifications(self, user):
        suratMasuk = SuratMasuk.objects.filter(upload_for=user)
        return suratMasuk.exclude(reader=user)

    def getFile(self, url):
        fl = File.objects.get(fileName=url)
        return fl

    def getSuratMasukByUrl(self, url):
        return SuratMasuk.objects.get(url=url)

    def checkApproving(self, sm_list, user):
        return sm_list.exclude(approve_by=user)

    def delete(self, fl):
        try:
            obj = SuratMasuk.objects.get(url=fl)
            obj.status = False
            obj.save()
        except:
            obj = SuratKeluar.objects.get(url=fl)
            obj.status = False
            obj.save()
        return True   

    def deleteArsip(self, fl):
        try:
            obj = Arsip.objects.get(url=fl)
            obj.status = False
            obj.save()
        except:
            pass
        return True   

    def addSuratKeluar(self, files, form_berkas):
        file = []
        fileName = str(form_berkas['fileName'].value()).upper()
        url = fileName.replace(' ', '-').lower()
        perihal = str(form_berkas['perihal'].value()).upper()
        nomor_surat = str(form_berkas['nomor_surat'].value()).upper()
        typeBerkas = str(form_berkas['typeBerkas'].value()).upper()
        destination = str(form_berkas['des'].value().upper()).upper()
        dest = str(form_berkas['address'].value()).upper()
        jenisBerkas = JenisBerkas.objects.get(jenisName=form_berkas['jenisBerkas'].value())
        #created = datetime.date.today().strftime('%d/%m/%Y')
        created = str(form_berkas['created_at'].value())
        
        for f in files:
            obj = File(file=f, fileName=url)
            obj.save()
            file.append(obj)

        surat = SuratKeluar(fileName=fileName, url=url, perihal=perihal, nomor_surat=nomor_surat, jenisBerkas=jenisBerkas, typeBerkas=typeBerkas, destination_address=dest, destination=destination, created_at=created)
        surat.save()
        arsip = Arsip(
                        fileName=fileName,
                        perihal=perihal,
                        nomor_surat=nomor_surat,
                        typeBerkas=typeBerkas,
                        group='SK',
                        url=url,
                        created_at=created,
                    )
        arsip.save()
        for fl in file:
            surat.file.add(fl)
            arsip.file_path.add(fl)
            surat.save()
            arsip.save()
        return True

    def addSuratMasuk(self, files, form_berkas):
        file = []
        department_list = []
        upload_for_list = []
        fileName = str(form_berkas['fileName'].value()).upper()
        url = (fileName.replace(' ', '-').lower())
        perihal = str(form_berkas['perihal'].value()).upper()
        nomor_surat = str(form_berkas['nomor_surat'].value()).upper()
        typeBerkas = form_berkas['typeBerkas'].value()
        upload_for = form_berkas['upload_for'].value()
        address_sender = str(form_berkas['address_sender'].value()).upper()
        sender = str(form_berkas['sender'].value()).upper()
        jenisBerkas = JenisBerkas.objects.get(jenisName=form_berkas['jenisBerkas'].value())
        #created = datetime.date.today().strftime('%d/%m/%Y')
        created = str(form_berkas['created_at'].value())
        department = Department.objects.all()

        for user in upload_for:
            userobj = Pengguna.objects.get(username=user)
            upload_for_list.append(userobj)

        for f in files:
            obj = File(file=f, fileName=url)
            obj.save()
            file.append(obj)

        surat = SuratMasuk(fileName=fileName, url=url, perihal=perihal, nomor_surat=nomor_surat, jenisBerkas=jenisBerkas, typeBerkas=typeBerkas, address_sender=address_sender, sender=sender, created_at=created)
        surat.save()
        for i in department:
            surat.department.add(i)
        for person in upload_for_list:
            surat.upload_for.add(person)
        for fl in file:
            surat.file.add(fl)
        return True

    def addPengguna(self, form_register):
        username = str(form_register['username'].value())
        password = str(form_register['password'].value())
        nik = str(form_register['nik'].value())
        firstName = str(form_register['firstName'].value()).upper()
        lastName = str(form_register['lastName'].value()).upper()
        role = str(form_register['role'].value())
        department = form_register['department'].value()
        divisi = str(form_register['divisi'].value())
        roles = Role.objects.get(roleName=role)
        divisis = Divisi.objects.get(divisiID=divisi)

        print(department)

        try:
            #get department obj
            dobj = Department.objects.get(departementID=department[0])
            person = Pengguna(
                username=username,
                password=password,
                firstName=str(firstName).capitalize(),
                lastName=str(lastName).capitalize(),
                role=roles,
                nik=nik,
                qr_code=self.randNum(),
            )
            person.save()
            person.department.add(dobj)
            person.divisi.add(divisis)
            person.save()
            return (True, 'Succes')
        except:
            return (False, 'gagal')
        
