from django.shortcuts import render, redirect
from HealthNet.models import Log
from django.utils import timezone
from HealthNet.forms import AppointmentPatientForm, AppointmentDoctorForm, AppointmentNurseForm
from HealthNet.models import PatientProfile, DoctorProfile, NurseProfile

# separate view for each user due to time constraints, will change later


'''
View for a patient to make an appointment
'''
def makeappointmentpatient(request):
    user = request.user
    created = False
    conflict = False

    if not user.is_authenticated():
        return redirect('/login')

    patient = PatientProfile.objects.get(patient=user)

    # process posted appt data
    if request.method == 'POST':
        appointmentForm = AppointmentPatientForm(data=request.POST)

        if appointmentForm.is_valid():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Make appointment'
            log.save()

            appointment = appointmentForm.save(commit=False)
            appointment.patient = patient

            appointment.hospital = appointmentForm.cleaned_data['doctor'].hospital
            appointment.patient_name = str(request.user.first_name) + ' ' + str(request.user.last_name)
            appointment.doctor_name = str(appointmentForm.cleaned_data['doctor'].doctor.first_name) + ' ' \
                + str(appointmentForm.cleaned_data['doctor'].doctor.last_name)
            appointment.hospital_name = appointment.hospital.name

            if not appointment.checkAppointment():
                conflict = True
                context = {'appointmentForm': appointmentForm, 'created':created,
                           'conflict': conflict}
                return context

            appointment.save()
            created = True
    else:
        appointmentForm = AppointmentPatientForm()

    context = {'appointmentForm': appointmentForm, 'created':created, 'conflict': conflict}
    return context

'''
Make appointment view for a doctor
'''
def makeappointmentdoctor(request):
    user = request.user
    created = False
    conflict = False

    if not user.is_authenticated():
        return redirect('/login')

    doctor = DoctorProfile.objects.get(doctor=user)

    if request.method == 'POST':
        appointmentForm = AppointmentDoctorForm(data=request.POST)

        if appointmentForm.is_valid():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Make appointment'
            log.save()

            appointment = appointmentForm.save(commit=False)
            appointment.doctor = doctor

            appointment.hospital = appointment.doctor.hospital
            appointment.patient_name = str(appointmentForm.cleaned_data['patient'].patient.first_name) \
                + ' ' + str(appointmentForm.cleaned_data['patient'].patient.last_name)
            appointment.doctor_name = str(appointment.doctor.doctor.first_name) + ' ' \
                + str(appointment.doctor.doctor.last_name)
            appointment.hospital_name = appointment.hospital.name

            if not appointment.checkAppointment():
                conflict = True
                context = {'doctor': doctor, 'appointmentForm': appointmentForm, 'created': created,
                           'conflict': conflict}
                return context

            appointment.save()

            created = True
    else:
        appointmentForm = AppointmentDoctorForm()

    context = {'doctor': doctor, 'appointmentForm': appointmentForm, 'created': created, 'conflict': conflict}
    return context

'''
Make appointment view for a nurse
'''
def makeappointmentnurse(request):
    user = request.user
    created = False
    conflict = False

    if not user.is_authenticated():
        return redirect('/login')

    nurse = NurseProfile.objects.get(nurse=user)

    if request.method == 'POST':
        appointmentForm = AppointmentNurseForm(data=request.POST)

        if appointmentForm.is_valid():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Make appointment'
            log.save()

            appointment = appointmentForm.save(commit=False)
            appointment.doctor = appointmentForm.cleaned_data['doctor']
            appointment.patient = appointmentForm.cleaned_data['patient']

            appointment.hospital = appointment.doctor.hospital
            appointment.patient_name = str(appointmentForm.cleaned_data['patient'].patient.first_name) \
                + ' ' + str(appointmentForm.cleaned_data['patient'].patient.last_name)
            appointment.doctor_name = str(appointmentForm.cleaned_data['doctor'].doctor.first_name) + ' ' \
                + str(appointmentForm.cleaned_data['doctor'].doctor.last_name)
            appointment.hospital_name = appointment.hospital.name

            if not appointment.checkAppointment():
                conflict = True
                context = {'nurse': nurse, 'appointmentForm': appointmentForm, 'created': created,
                           'conflict': conflict}
                return context

            appointment.save()

            created = True
    else:
        appointmentForm = AppointmentNurseForm()

    context = {'nurse': nurse, 'appointmentForm': appointmentForm, 'created': created, 'conflict': conflict}
    return context
