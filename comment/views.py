from django.shortcuts import render, redirect
from prescription.forms import PrescriptionForm
from HealthNet.models import PatientProfile, Prescription, User, TestModel
from django.utils import timezone
from comment.forms import CommentForm

# Create your views here.
def comment(request):
    id = int(request.GET.get("patient"))
    testId = int(request.GET.get("testId"))

    user = User.objects.get(id = id)

    if(request.user.is_authenticated()):
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.patient = PatientProfile.objects.get(patient=user)
                comment.test = TestModel.objects.get(id = testId)
                comment.author = User.objects.get(id=request.user.id)
                comment.save()
        else:
            form = CommentForm()

        if request.user.groups.filter(name="Doctors").exists() or request.user.groups.filter(name="Nurses").exists():
            return redirect('/viewprofile?patient=' + str(id) + '#tests')
        else:
            return redirect('HealthNet/#tests')
    else:
        return redirect('/login')


def deleteComment(request):
    deleted = False
    pId = request.GET.get('pId')
    prescription = Prescription.objects.get(id=pId)
    if request.user.is_authenticated():
        if request.method == 'POST':
            prescription.delete()
            deleted = True
    else:
        return redirect('/login')
