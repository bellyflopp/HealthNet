from django.shortcuts import render, redirect
from prescription.forms import PrescriptionForm
from HealthNet.models import DoctorProfile, Prescription, Log
from django.utils import timezone

# Create your views here.
def makePrescription(request, patient):
    created = False
    if(request.user.is_authenticated()):
        if request.method == 'POST':
            form = PrescriptionForm(data=request.POST)
            if form.is_valid():
                prescription = form.save(commit=False)
                prescription.patient = patient
                prescription.doctor = DoctorProfile.objects.get(doctor=request.user)
                prescription.date = timezone.now()
                prescription.save()

                log = Log()
                log.user = request.user
                log.username = request.user.username
                log.time = timezone.now()
                log.type = 'Create Prescription'
                log.save()

                created = True
        else:
            form = PrescriptionForm()

        return {'created': created, 'prescriptionForm': form}
    else:
        return redirect('/login')


def deletePrescription(request):
    deleted = False
    pId = request.GET.get('pId')
    prescription = Prescription.objects.get(id=pId)
    if request.user.is_authenticated():
        if request.method == 'POST':
            prescription.delete()
            deleted = True
    else:
        return redirect('/login')



