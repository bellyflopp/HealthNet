from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from HealthNet.models import Log, DoctorProfile, NurseProfile, PatientProfile
from register.forms import PatientProfileForm
from modprofile.forms import UserForm
from django.utils import timezone


# Create your views here.
'''
view for user login
'''
def user_login(request):
    if request.user.is_authenticated():#redirects to appropriate page for already logged in user
        user = request.user

        # log usage
        log = Log()
        log.user = request.user
        log.username = request.user.username
        log.time = timezone.now()
        log.type = 'Login'
        log.save()

        # send user to correct home page
        if request.user.is_superuser:
            return HttpResponseRedirect('/admin/home')
        elif request.user.groups.filter(name='Doctors').exists():
            return HttpResponseRedirect('/doctor')
        elif request.user.groups.filter(name='Nurses').exists():
            return HttpResponseRedirect('/nurse')
        else:
            patient = PatientProfile.objects.get(patient=user)
            userForm = UserForm(instance=user)
            profileForm = PatientProfileForm(instance=patient)
            context = {'patient': patient, 'userForm': userForm, 'profileForm': profileForm}
            return HttpResponseRedirect('/HealthNet/', context)
    else:

        valid = True

        if request.method == 'POST':

            # get username and pass from request
            username = request.POST.get('username')
            password = request.POST.get('password')

            # log user in
            user = authenticate(username=username, password=password)

            # send user to correct page after login
            if user:
                if user.is_superuser:
                    login(request, user)
                    return HttpResponseRedirect('/admin/home')
                elif user.is_active:
                    log = Log()
                    log.user = user
                    log.username = user.username
                    log.time = timezone.now()
                    log.type = 'Login'
                    log.save()

                    login(request, user)

                    if(NurseProfile.objects.filter(nurse__id=user.id).exists()):
                        return HttpResponseRedirect('/nurse')
                    elif(DoctorProfile.objects.filter(doctor__id=user.id).exists()):
                        return HttpResponseRedirect('/doctor')
                    else:
                        patient = PatientProfile.objects.get(patient=user)
                        userForm = UserForm(instance=user)
                        profileForm = PatientProfileForm(instance=patient)
                        context = {'patient': patient, 'userForm': userForm, 'profileForm': profileForm}
                        return HttpResponseRedirect('/HealthNet', context)

                    #if user.groups.filter(name='Doctors').exists():
                    #    return HttpResponseRedirect('/doctor')
                    #elif user.groups.filter(name='Nurses').exists():
                    #    return HttpResponseRedirect('/nurse')
                    #else:
                    #    return HttpResponseRedirect('/HealthNet/')
                else:
                    return HttpResponse("Your HealthNet account is not active.")

            else:
                print("Invalid login details: {0}, {1}".format(username, password))
                valid = False
                return render(request, 'HealthNet/login.html', {'valid': valid})

        else:
            # nothing posted to page, prompt user for a login
             return render(request, 'HealthNet/login.html', {'valid': valid})
