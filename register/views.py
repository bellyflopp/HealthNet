from django.shortcuts import render
from register.forms import UserForm, PatientProfileForm, PatientMedicalForm
from django.contrib.auth import logout
from HealthNet.models import Log,DoctorProfile
from django.utils import timezone


# Create your views here.

'''
View for registering a new profile
'''
def register(request):
    if request.user.is_authenticated():
        logout(request)

    registered = False

    if request.method == 'POST':
        userForm = UserForm(data=request.POST)
        profileForm = PatientProfileForm(data=request.POST)
        medicalForm = PatientMedicalForm(data=request.POST)
        log = Log()

        if userForm.is_valid() and profileForm.is_valid() and medicalForm.is_valid():
            print("valid")
            patient = userForm.save()

            patient.set_password(patient.password)
            patient.save()

            profile = profileForm.save(commit=False)
            medProfile = medicalForm.save(commit=False)

            profile.patient = patient

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.height = medProfile.height
            profile.weight = medProfile.weight
            profile.insuranceNum = medProfile.insuranceNum
            profile.doctor = medProfile.doctor
            profile.hospital = medProfile.hospital
            profile.bloodType = medProfile.bloodType
            profile.emergencyContactFirst = medProfile.emergencyContactFirst
            profile.emergencyContactLast = medProfile.emergencyContactLast
            profile.emergencyContactEmail = medProfile.emergencyContactEmail
            profile.emergencyContactPhone = medProfile.emergencyContactPhone

            profile.save()

            registered = True

            log.user = profile.patient
            log.username = profile.patient.username
            log.time = timezone.now()
            log.type = 'Patient register'

            log.save()

        else:
            print(userForm.errors, profileForm.errors, medicalForm.errors)

    else:
        userForm = UserForm()
        profileForm = PatientProfileForm()
        medicalForm = PatientMedicalForm()

    return render(request, 'HealthNet/register.html',
                  {'userForm': userForm, 'profileForm': profileForm, 'medicalForm': medicalForm, 'registered': registered})