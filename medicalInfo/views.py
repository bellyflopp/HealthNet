from django.shortcuts import render, redirect
from HealthNet.models import PatientProfile
from register.forms import UserForm, PatientMedicalForm, ModEmergencyContactForm, ModMedicalForm
from HealthNet.models import Log, User
from django.utils import timezone

# Create your views here.
def medical(request):
    user = request.user

    if not user.is_authenticated():
        return redirect('/login')

 #   if request.user.groups.filter(name='Doctors').exists() or user.groups.filter(name='Nurses').exists():
 #           return redirect('/doctor')


    patient = PatientProfile.objects.get(patient=user)
    medForm = PatientMedicalForm(instance=patient)

    context = {'medForm': medForm}
    return context


def modMedical(request, patient):
    id=int(request.GET.get("patient"))
    user = User.objects.get(id=id)
    patient = PatientProfile.objects.get(patient=user)

    if request.method == "POST":
        medForm=ModMedicalForm(data=request.POST, instance=patient)

        if medForm.is_valid():
            form=medForm.save()

            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Modify Medical Information'
            log.save()

            form.save()
        else:
            print(medForm.errors)
    else:
        medForm=ModMedicalForm(instance=patient)

    context={'medForm': medForm}
    return context

def modEmergencyContact(request):
    user = request.user
    patient = PatientProfile.objects.get(patient=user)

    # redirect if user isn't logged in
    if not user.is_authenticated():
        return redirect('/login')

    if request.method == "POST":
        contactForm = ModEmergencyContactForm(data=request.POST, instance=patient)

        if contactForm.is_valid():
            form = contactForm.save()

            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Modify Emergency Contact'
            log.save()

            form.save()

        else:
            print(contactForm.errors)

    else:
        contactForm = ModEmergencyContactForm(instance=patient)

    context = {'emergencyContactForm': contactForm}
    return context
