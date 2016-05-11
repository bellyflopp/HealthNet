from django.shortcuts import render,redirect
from HealthNet.models import Log,Appointment,DoctorProfile,PatientProfile,NurseProfile
from django.utils import timezone
from HealthNet.forms import *

# Create your views here.
'''
View for calendar, uses the fullcalendar.io javascript library on the html page
'''
def calendar(request):
    user = request.user

    # send user to login if not logged in
    if not user.is_authenticated():
        return redirect('/login')
    else:
        # figure out user type
        type = None

        if(PatientProfile.objects.filter(patient__id=user.id).exists()):
            type = 'patient'
        elif(DoctorProfile.objects.filter(doctor__id=user.id).exists()):
            type = 'doctor'
        elif(NurseProfile.objects.filter(nurse__id=user.id).exists()):
            type = 'nurse'
        else:
            type = 'null'

        # get appointments pertaining to the user

        appointments = {}

        if(type=='doctor'):
            appointments = Appointment.objects.filter(doctor__doctor__id=user.id)

        elif(type=='nurse'):
            appointments = Appointment.objects.all()

        elif(type=='patient'):
            appointments = Appointment.objects.filter(patient__patient__id=user.id)

        appointmentForms = {}
        for app in appointments:
            appointmentForms[app.__str__()] = AppointmentPatientForm(app)

        # render the page and pass the appts to the template
        context = {'type': type, 'appointments':appointments, 'appointmentForms':appointmentForms}
        return context