from django.shortcuts import render, redirect
from django.contrib.auth import logout
from HealthNet.models import Log
from django.utils import timezone
from modprofile.views import *
from cal.views import *
from makeappointment.views import *
from modappointment.views import *
from message.views import *
from medicalInfo.views import *
from HealthNet.forms import *
from HealthNet.static.reportlab.platypus import doctemplate,paragraph
from HealthNet.static.reportlab.lib.styles import *
from HealthNet.static.reportlab.lib.pagesizes import letter
from django.http import HttpResponse, HttpResponseRedirect
from io import BytesIO
from testresult.views import testsHome
import re
from collections import OrderedDict
from operator import itemgetter

'''
redirect for blank page (nothing after ip)
'''
def blank(request):
    return redirect('HealthNet/')

'''
redirect for home page
'''
def home(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('/admin/home')
        elif request.user.groups.filter(name='Doctors').exists():
            return redirect('/doctor')
        elif request.user.groups.filter(name='Nurses').exists():
            return redirect('/nurse')
        else:
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'View Home'
            log.save()
            contextCalendar = calendar(request)
            #render(request, 'HealthNet/calendar.html', contextCalendar)

            #contextViewprofile = viewprofile(request)
            # render(request, 'HealthNet/calendar.html', contextViewprofile)

            contextMakeAppointment = makeappointmentpatient(request)
            # render(request, 'HealthNet/calendar.html', contextMakeAppointment)

            #contextModAppointment = modappointment(request)
            # render(request, 'HealthNet/modappointment.html', contextModAppointment)

            contextMessage=message(request)
            # render(request, 'HealthNet/message.html', contextMessage)

            contextMedical=medical(request)
            #contextModProfile = modprofile(request)
            contextModProfile=modprofile(request)
            contextModEmergencyContact=modEmergencyContact(request)

            context = contextCalendar
            #context.update(contextViewprofile)
            context.update(contextMakeAppointment)
            context.update(contextMessage)
            context.update(contextMedical)
            context.update(contextModProfile)
            context.update(contextModEmergencyContact)

            patient = PatientProfile.objects.get(patient=request.user)
            completed = TestModel.objects.all().filter(patient=patient, isReleased=True)
            pending = TestModel.objects.all().filter(patient=patient, isReleased=False)
            prescriptions = Prescription.objects.all().filter(patient=patient)
            news = News.objects.latest(field_name='date')
            comments = Comment.objects.all().filter(patient=patient)
            commentForm = CommentForm(data=request.POST)

            completedfiles = {}
            pendingfiles = {}
            for test in completed:
                completedfiles.__setitem__(test.id, FileUpload.objects.all().filter(test=test))
            for test in pending:
                pendingfiles.__setitem__(test.id, FileUpload.objects.all().filter(test=test))

            context['patient'] = patient
            context['user'] = request.user
            context['type'] = 'patient'
            context['completed'] = completed
            context['pending'] = pending
            context['prescriptions'] = prescriptions
            context['completedfiles'] = completedfiles
            context['pendingfiles'] = pendingfiles
            context['comments'] = comments
            context['commentForm'] = commentForm
            context['news'] = news
            #render(request, 'HealthNet/calendar.html', contextCalendar)

            return render(request, 'HealthNet/home.html', context)
    else:
        return redirect('/login/')

'''
redirect for doctor home page
'''
def doctor(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('/admin/home')
        elif request.user.groups.filter(name='Doctors').exists():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'View Home'
            log.save()
            contextCalendar = calendar(request)
            #render(request, 'HealthNet/calendar.html', contextCalendar)

            contextMakeAppointment = makeappointmentdoctor(request)
            # render(request, 'HealthNet/calendar.html', contextMakeAppointment)

            # contextModAppointment = modappointment(request)
            # render(request, 'HealthNet/modappointment.html', contextModAppointment)

            contextMessage=message(request)
            # render(request, 'HealthNet/message.html', contextMessage)

            contextTests=testsHome(request)

            context = contextCalendar
            context.update(contextMakeAppointment)
            # context.update(contextModAppointment)
            context.update(contextMessage)
            context.update(contextTests)

            news = News.objects.latest(field_name='date')

            doctor = DoctorProfile.objects.get(doctor=request.user)
            context['doctor'] = doctor
            context['user'] = request.user
            context['type'] = 'doctor'
            context['patients'] = PatientProfile.objects.filter(doctor=doctor)
            context['all'] = PatientProfile.objects.all()
            context['news'] = news


            #render(request, 'HealthNet/calendar.html', context)
            return render(request, 'HealthNet/doctor.html', context)
        elif request.user.groups.filter(name='Nurses').exists():
            redirect('/nurse')
        else:
            return redirect('/HealthNet/')
    else:
        return redirect('/login/')

'''
redirect for nurse home page
'''
def nurse(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return redirect('/admin/home')
        elif request.user.groups.filter(name='Nurses').exists():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'View Home'
            log.save()
            contextCalendar = calendar(request)
            #render(request, 'HealthNet/calendar.html', contextCalendar)

            contextMakeAppointment = makeappointmentnurse(request)
            # render(request, 'HealthNet/calendar.html', contextMakeAppointment)

            # contextModAppointment = modappointment(request)
            # render(request, 'HealthNet/modappointment.html', contextModAppointment)

            contextMessage=message(request)
            # render(request, 'HealthNet/message.html', contextMessage)


            context = contextCalendar
            context.update(contextMakeAppointment)
            # context.update(contextModAppointment)
            context.update(contextMessage)
            news = News.objects.latest(field_name='date')


            nurse = NurseProfile.objects.get(nurse=request.user)
            context['nurse'] = nurse
            context['user'] = request.user
            context['type'] = 'nurse'
            context['patients'] = PatientProfile.objects.filter(hospital=nurse.hospital)
            context['news'] = news



            #render(request, 'HealthNet/calendar.html', context)
            return render(request, 'HealthNet/nurse.html', context)
        elif request.user.groups.filter(name='Doctors').exists():
            redirect('/doctor')
        else:
            return redirect('/HealthNet/')
    else:
        return redirect('/login/')


'''
redirect for user logout
'''
def user_logout(request):
    if request.user.is_authenticated():
        log = Log()
        log.user = request.user
        log.username = request.user.username
        log.time = timezone.now()
        log.type = 'Logout'
        log.save()

        logout(request)
        return redirect('/login/')
    else:
        return redirect('/login/')

'''
redirect for r2 page
'''
def r2(request):
    return render(request, 'HealthNet/r2.html')

'''
redirect if url is invalid
'''
def invalid(request):
    return redirect('/HealthNet/')

def statistics(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        pageviews = Log.objects.filter(type__startswith='View').count()#just preform operations on system logs
        users = User.objects.all().count()

        # gather the top 3 visit reasons

        drugs=Prescription.objects.all()
        drugQuantities = {}

        for drug in drugs:
            if drug.name in drugQuantities:
                drugQuantities[drug.name] += 1
            else:
                drugQuantities[drug.name] = 1

        sorted_drugs = OrderedDict(sorted(drugQuantities.items(),key=itemgetter(1)))


        context = {'pageviews': pageviews, 'users': users, 'sorted_drugs':sorted_drugs}#then add to context
        return render(request, 'admin/statistics.html', context)#then render the page
    else:
        return redirect('/login/')

def adminhome(request):
    if request.user.is_authenticated() and request.user.is_superuser:
        return render(request, 'admin/home.html')
    else:
        return redirect('/login/')

def upload(request):
    testId = int(request.GET.get('testId'))
    patientId = int(request.GET.get('patient'))
    if request.user.is_authenticated():
        if request.method == 'POST':
            fileForm = uploadForm(request.POST, request.FILES)
            print(fileForm.errors)
            if fileForm.is_valid():
                log = Log()
                log.user = request.user
                log.username = request.user.username
                log.time = timezone.now()
                log.type = 'Upload Document'
                log.save()
                test = TestModel.objects.get(id=testId)

                files = FileUpload.objects.all().filter(test=test)

                shortName = request.FILES['file'].name.split('/')[-1].replace(' ','_')
                shortName = re.sub('[^a-zA-Z0-9\-_ \n\.]','',shortName)
                file = FileUpload(file=request.FILES['file'], user=request.user, userid=request.user.id, test=test, shortname=shortName)
                file.save()
                return render(request, "HealthNet/upload.html", {'uploaded': True, 'testId': testId, 'testFiles':files, 'patientId': patientId, 'fileForm': uploadForm()})
            else:
                test = TestModel.objects.get(id=testId)
                files = FileUpload.objects.all().filter(test=test)
                return render(request, "HealthNet/upload.html", {'fileForm': uploadForm(), 'uploaded': False, 'testId': testId, 'patientId': patientId, 'testFiles': files})
        else:
            test = TestModel.objects.get(id=testId)
            files = FileUpload.objects.all().filter(test=test)
            context = {'fileForm': uploadForm(), 'uploaded': False, 'testId': testId, 'testFiles': files, 'patientId': patientId}
            return render(request, "HealthNet/upload.html", context)
    else:
        return redirect('/login/')

def serveFile(request):
    if request.user.is_authenticated():
        file = request.GET.get('filename')
        id = int(request.GET.get('userid'))
        if(id == request.user.id):
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Download File'
            log.save()
            url = "/download/uploads/user_%s/%s" % (id, file)
            return redirect(url)
        elif not (request.user.groups.filter(name="Doctors").exists() or request.user.groups.filter(name="Nurses").exists()):
            patient = PatientProfile.objects.get(patient=User.objects.get(id=request.user.id))
            doctor = DoctorProfile.objects.get(doctor=User.objects.get(id=id))
            print(patient.doctor == doctor)
            if(patient.doctor == doctor):
                log = Log()
                log.user = request.user
                log.username = request.user.username
                log.time = timezone.now()
                log.type = 'Download File'
                log.save()
                url = "/download/uploads/user_%s/%s" % (id, file)
                return redirect(url)
        else:
            return redirect('/HealthNet/')
    else:
        return redirect('/login/')

def exportData(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="HealthNet Data Export.pdf"'

    buffer = BytesIO()

    page = doctemplate.SimpleDocTemplate(buffer,
                                      rightMargin=72,
                                      leftMargin=72,
                                      topMargin=72,
                                      bottomMargin=72,
                                      pagesize=letter)

    elements = []

    styles = getSampleStyleSheet()

    user = request.user
    patient = PatientProfile.objects.get(patient=user)

    elements.append(paragraph.Paragraph('Profile Information', styles['Heading1']))
    name = "Name: " + patient.patient.first_name + " " + patient.patient.last_name
    elements.append(paragraph.Paragraph(name, styles['Normal']))
    gender = "Gender: " + patient.gender
    elements.append(paragraph.Paragraph(gender, styles['Normal']))
    phone = "Phone Number: " + str(patient.phone)
    elements.append(paragraph.Paragraph(phone, styles['Normal']))
    address = "Address: " + str(patient.houseNumber) + " " + patient.street
    elements.append(paragraph.Paragraph(address, styles['Normal']))
    town = "Town: " + patient.town
    elements.append(paragraph.Paragraph(town, styles['Normal']))
    state = "State: " + patient.state
    elements.append(paragraph.Paragraph(state, styles['Normal']))
    zip = "Zip: " + str(patient.zip)
    elements.append(paragraph.Paragraph(zip, styles['Normal']))

    elements.append(paragraph.Paragraph('Medical Information', styles['Heading1']))
    height = "Height: " + str(patient.height)
    elements.append(paragraph.Paragraph(height, styles['Normal']))
    weight = "Weight: " + str(patient.weight)
    elements.append(paragraph.Paragraph(weight, styles['Normal']))
    bloodType = "Blood Type: " + patient.bloodType
    elements.append(paragraph.Paragraph(bloodType, styles['Normal']))
    doc = patient.doctor
    doctor = "Doctor: " + doc.doctor.first_name + " " + doc.doctor.last_name
    elements.append(paragraph.Paragraph(doctor, styles['Normal']))
    hos = patient.hospital
    hospital = "Hospital: " + hos.name
    elements.append(paragraph.Paragraph(hospital, styles['Normal']))
    emcontact = "Emergency Contact: " + patient.emergencyContactFirst + " " + patient.emergencyContactLast
    elements.append(paragraph.Paragraph(emcontact, styles['Normal']))

    elements.append(paragraph.Paragraph('Prescriptions', styles['Heading1']))
    prescriptions = Prescription.objects.all().filter(patient=patient)
    for prescription in prescriptions:
        elements.append(paragraph.Paragraph(prescription.name, styles['Normal']))

    elements.append(paragraph.Paragraph('Tests', styles['Heading1']))
    tests = TestModel.objects.all().filter(patient=patient)
    for test in tests:
        elements.append(paragraph.Paragraph(test.testName, styles['Normal']))
        if test.isReleased:
            result = "Result: " + test.result
            elements.append(paragraph.Paragraph("Status: Released", styles['Normal']))
            elements.append(paragraph.Paragraph(result, styles['Normal']))
        else:
            elements.append(paragraph.Paragraph("Status: Pending", styles['Normal']))

    page.build(elements)



    log = Log()
    log.user = request.user
    log.username = request.user.username
    log.time = timezone.now()
    log.type = 'Export Information'
    log.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

'''
View that handles transferring a patient. Expects the url arguments:

hospitalId: id of the hospital to be transferred to
patientId: id of the patient to be transferred
doctorId: id of the doctor being assigned

On call, performs backend calls then redirects to the page the user was already
on

Note: if a user manually enters in the url, there's nothing to stop them.
'''
def transfer(request):

    hosId=request.GET.get('hospitalId',None)
    patId=request.GET.get('patientId',None)
    docId=request.GET.get('doctorId',None)

    # if any of the arguments are 'none' or not provided, then the transfer can't happen
    if( not (hosId and patId and docId) ):
        print("Error, some or all arguments for a transfer aren't provided")
        print(hosId)
        print(patId)
        print(docId)
        return redirect('/doctor/#patients')

    hosId=int(hosId)
    patId=int(patId)
    docId=int(docId)

    # check to see if the hospital, patient, and doctor all exist in the database
    if( not (
            Hospital.objects.filter(id=hosId).exists() and
            PatientProfile.objects.filter(id=patId).exists() and
            DoctorProfile.objects.filter(id=docId).exists()
            )
    ):
        print("Error, some or all of the models do not exist in the database.")
        return redirect('/doctor/#patients')

    hospital = Hospital.objects.get(id=hosId)

    hospital.transferPatient(PatientProfile.objects.get(id=patId),DoctorProfile.objects.get(id=docId))

    print(PatientProfile.objects.get(id=patId).doctor)
    print(PatientProfile.objects.get(id=patId).hospital)

    log = Log()
    log.user = request.user
    log.username = request.user.username
    log.time = timezone.now()
    log.type = 'Patient Transfer'
    log.save()

    return redirect('/doctor/#patients')