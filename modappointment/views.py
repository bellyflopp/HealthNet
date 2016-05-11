from django.shortcuts import render, redirect
from HealthNet.forms import *
from HealthNet.models import *
from django.utils import timezone


# Create your views here.
def modappointment(request):
    modified = False
    newConflict = False
    user = request.user
    appointmentNum = request.GET.get('app_id')
    delete = request.GET.get('delete')
    try:
        appointment = Appointment.objects.get(id=appointmentNum)
    except:
        appointment = Appointment.__new__()
    type = ''

    if not user.is_authenticated():
        return redirect('/login')

    if delete == 'true':
        return delappointment(request)

    if request.method != "POST":
        log = Log()
        log.user = request.user
        log.username = request.user.username
        log.time = timezone.now()
        log.type = 'View edit appointment'
        log.save()

    if request.method == "POST":
        if request.user.groups.filter(name='Doctors').exists():
            appointmentForm = AppointmentDoctorForm(data=request.POST, instance=appointment)
            doctor = DoctorProfile.objects.get(doctor=user)
        elif request.user.groups.filter(name='Nurses').exists():
            appointmentForm = AppointmentNurseForm(data=request.POST, instance=appointment)
            nurse = NurseProfile.objects.get(nurse=user)
        else:
            appointmentForm = AppointmentPatientForm(data=request.POST, instance=appointment)
            patient = PatientProfile.objects.get(patient=user)

        if appointmentForm.is_valid():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Edit Appointment'
            log.save()

            if request.user.groups.filter(name='Doctors').exists():
                appointment = appointmentForm.save()

                if not appointment.checkAppointment():
                    newConflict = True
                    type = 'doctor'
                    context = {'doctor': doctor, 'appointmentForm': appointmentForm, 'modified': modified,
                        'newConflict': newConflict, 'id': appointmentNum, 'type': type}


                    return render(request, 'HealthNet/modappointment.html', context)

                appointment.save()

                modified = True
            elif request.user.groups.filter(name='Nurses').exists():
                appointment = appointmentForm.save()

                if not appointment.checkAppointment():
                    newConflict = True
                    type = 'nurse'
                    context = {'nurse': nurse, 'appointmentForm': appointmentForm, 'modified': modified,
                            'newConflict': newConflict, 'id': appointmentNum, 'type': type}

                    return render(request, 'HealthNet/modappointment.html', context)

                appointment.save()

                modified = True
            else:
                appointment = appointmentForm.save()

                if not appointment.checkAppointment():
                    newConflict = True
                    type = 'patient'
                    context = {'patient': patient, 'appointmentForm': appointmentForm, 'modified': modified,
                                'newConflict': newConflict, 'id': appointmentNum, 'type': type}

                    return render(request, 'HealthNet/modappointment.html', context)

                appointment.save()

                modified = True
        else:
            if request.user.groups.filter(name='Doctors').exists():
                type='doctor'
            elif request.user.groups.filter(name='Nurses').exists():
                type='nurse'
            else:
                type ='patient'

            print(appointmentForm.errors)
    else:
        if request.user.groups.filter(name='Doctors').exists():
            type = 'doctor'
            appointmentForm = AppointmentDoctorForm(instance=appointment)
        elif request.user.groups.filter(name='Nurses').exists():
            appointmentForm = AppointmentNurseForm(instance=appointment)
            type = 'nurse'
        else:
            appointmentForm = AppointmentPatientForm(instance=appointment)
            type = 'patient'

    context = {'appointment':appointment, 'appointmentForm': appointmentForm, 'modified':modified, 'newConflict': newConflict, 'id': appointmentNum,
               'type': type}

    return render(request, 'HealthNet/modappointment.html', context)

def delappointment(request):
    appointmentNum = request.GET.get('app_id')
    appointment = Appointment.objects.get(id=appointmentNum)
    appointment.delete()
    deleted = True
    context = {'deleted': deleted, 'id': appointmentNum}

    return render(request, 'HealthNet/modappointment.html', context)