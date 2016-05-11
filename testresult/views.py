from django.shortcuts import render, redirect
from testresult.forms import testForm
from HealthNet.models import Log, FileUpload, TestModel, DoctorProfile, PatientProfile, User
from django.utils import timezone

# Create your views here.
def testresult(request, patient, edited, justcreated):
    uploaded = False

    if request.user.is_authenticated():
        if request.method == 'POST' and not edited and not justcreated:
            form = testForm(data=request.POST)

            if form.is_valid():
                log = Log()
                log.user = request.user
                log.username = request.user.username
                log.time = timezone.now()
                log.type = 'Create test result'
                log.save()

                test = form.save(commit=False)
                test.patient = patient
                test.doctor = DoctorProfile.objects.get(doctor=request.user)
                test.save()

                form = testForm()

                uploaded = True
        else:
            form = testForm()

        context = {'testForm': form, 'uploaded': uploaded}
        return context

    else:
        return redirect('/login/')

def testsHome(request):
    if request.user.is_authenticated():
        tests = TestModel.objects.all().filter(doctor=DoctorProfile.objects.get(doctor=request.user))
        return {'testResults': tests}
    else:
        return redirect('/login/')

def testsFiles(request):
    testId = int(request.GET.get('testId'))
    if request.user.is_authenticated():
        test = TestModel.objects.get(id=testId)
        files = FileUpload.objects.all().filter(test=test)
        return render(request, 'HealthNet/testfiles.html', {'testFiles': files, 'testId': testId})
    else:
        return redirect('/login/')

def modTest(request):
    patient = User.objects.get(id=int(request.GET.get("patient")))
    profile = PatientProfile.objects.get(patient=patient)

    testId = int(request.GET.get('testId'))
    stringE = request.GET.get("edited")
    stringD = request.GET.get("delete")

    if stringD == 'True':
        delete = True
    else:
        delete = False

    if stringE == 'True':
        edited = True
    else:
        edited = False

    if request.user.is_authenticated():
        test = TestModel.objects.get(id=testId)

        if delete:
            test.delete()

        elif edited == False:
            modForm = testForm(instance=test)
            return render(request, 'HealthNet/edittest.html', {'patient': profile, 'modForm': modForm, 'testId': testId})

        elif request.method == 'POST':
            modForm = testForm(data=request.POST, instance=test)

            if modForm.is_valid():
                log = Log()
                log.user = request.user
                log.username = request.user.username
                log.time = timezone.now()
                log.type = 'Edit Test'
                log.save()

                modForm.save()

    else:
        return redirect('/login/')




def releasetest(request):
    testId = request.GET.get('testId')

    if request.user.is_authenticated():
        mytest = TestModel.objects.get(id=testId)
        mytest.isReleased = not(mytest.isReleased)

        log = Log()
        log.user = request.user
        log.username = request.user.username
        log.time = timezone.now()
        log.type = 'Release/Withdraw Test'
        log.save()

        mytest.save()
    else:
        return redirect('/login/')