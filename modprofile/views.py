from django.shortcuts import render, redirect
from register.forms import UserForm, PatientProfileForm, PatientMedicalForm, ModProfileForm
from modprofile.forms import UserForm
from HealthNet.models import *
from HealthNet.forms import VisitForm
from comment.forms import CommentForm
from prescription.views import *
from django.utils import timezone
from django.contrib.auth.models import User
from testresult.views import *
from medicalInfo.views import modMedical
from comment.views import *

# Create your views here.

'''
View to modify the profile
'''
def modprofile(request):
    updated = False

    user = request.user

    # redirect if user isn't logged in
    if not user.is_authenticated():
        return redirect('/login')

    patient = PatientProfile.objects.get(patient=user)

    # process posted data
    if request.method == "POST":
        userForm = UserForm(data=request.POST, instance=user)
        profileForm = ModProfileForm(data=request.POST, instance=patient)

        if userForm.is_valid() and profileForm.is_valid():
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'Edit Profile'
            log.save()

            user = userForm.save()
            user.save()

            patient.user = user
            patient = profileForm.save()
            patient.save()

            updated = True

        else:
            print(userForm.errors, profileForm.errors)

    else:
        userForm = UserForm(instance=user)
        profileForm = ModProfileForm(instance=patient)

    context = {'userForm': userForm, 'profileForm': profileForm, 'updated': updated, 'user': user}
    return context




def viewprofile(request):
    if request.user.is_authenticated():
        stringR = request.GET.get("releasing")
        stringE = request.GET.get("edited")
        stringD = request.GET.get("delete")
        stringC = request.GET.get("justcreated")
        commentBool = request.GET.get("comment")

        deletePre = request.GET.get("deleted")

        if stringR == 'True':
            releasing = True
        else:
            releasing = False

        if releasing:
            releasetest(request)

        if stringE == 'True':
            edited = True
        else:
            edited = False

        if stringD == 'True':
            delete = True
        else:
            delete = False

        if edited or delete:
            modTest(request)

        if deletePre == "True":
            deleteIt = True
        else:
            deleteIt = False

        if stringC == 'False':
            justcreated = False
        else:
            justcreated = True

        if commentBool == "True":
            commentThis = True
        else:
            commentThis = False

        if deleteIt:
            deletePrescription(request)

        id=int(request.GET.get("patient"))
        patient = User.objects.get(id=id)
        profile = PatientProfile.objects.get(patient=patient)


        resultContext = testresult(request, profile, edited, justcreated)


        completed = TestModel.objects.all().filter(patient=profile, isReleased=True)
        pending = TestModel.objects.all().filter(patient=profile, isReleased=False)
        completedfiles = {}
        pendingfiles = {}
        for test in completed:
            completedfiles.__setitem__(test.id, FileUpload.objects.all().filter(test=test))
        for test in pending:
            pendingfiles.__setitem__(test.id, FileUpload.objects.all().filter(test=test))
        prescriptions = Prescription.objects.all().filter(patient=profile)

        if request.user.groups.filter(name="Nurses").exists():
            type = 'nurse'
            viewer = NurseProfile.objects.get(nurse=request.user)
        else:
            type = 'doctor'
            viewer = DoctorProfile.objects.get(doctor=request.user)

        if type == 'doctor' and (viewer.hospital == profile.hospital or viewer == profile.doctor):
            same = True
        else:
            same = False

        comments = Comment.objects.all().filter(patient=profile)

        commentForm = CommentForm(data=request.POST)
        context = {'patient':profile, 'type':type, 'completed':completed, 'pending': pending,
                   'same':same, 'completedfiles': completedfiles, 'pendingfiles': pendingfiles,'prescriptions':prescriptions, 'commentForm': commentForm, 'comments':comments}
        context.update(resultContext)

        if request.user.groups.filter(name="Doctors").exists():
            doctor = viewer
            context['doctor'] = doctor

        context.update(makePrescription(request, profile))
        context.update(admit(request, profile))
        context.update(modMedical(request, patient))

        if not justcreated:
            url = "/viewprofile?patient=%s&releasing=False&justcreated=True#tests" % id
            return redirect(url)
        else:
            log = Log()
            log.user = request.user
            log.username = request.user.username
            log.time = timezone.now()
            log.type = 'View Patient Medical Info'
            log.save()

            return render(request, 'HealthNet/viewprofile.html', context)
    else:
        return redirect('/login/')


'''
View for admitting a patient. Expects a url argument specifying the patient id
?patientId=<id>
'''
def admit(request, patient):

    if (request.user.is_authenticated()):
        if request.method == "POST":
            form = VisitForm(data=request.POST)

            if form.is_valid():
                visit = form.save(commit=False)
                visit.patient = patient
                visit.admitDate = timezone.now()
                form.save()

                patient.admissionStatus = True
                patient.save()
        else:
            form = VisitForm()
    else:
        return redirect('/login')

    context = {'visitForm': form}
    return context

def discharge(request):

    user = User.objects.get(id=int(request.GET.get("patient")))
    patient = PatientProfile.objects.get(patient=user)

    if (request.user.is_authenticated()):
        patient.admissionStatus = False
        patient.save()

        return redirect("/viewprofile?patient=" + request.GET.get("patient") + "#profile")
    else:
        return redirect('/login')
