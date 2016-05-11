from django import forms
from django.contrib.auth.models import User
from HealthNet.models import PatientProfile, TestModel, Prescription


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class PatientProfileForm(forms.ModelForm):

    class Meta:
        model = PatientProfile
        fields = ('birthday', 'gender', 'phone', 'houseNumber', 'street', 'town', 'state', 'zip')
        execlude = ['user']

#    def __init__(self, patient, *args, **kwargs):
#        super(PatientProfileForm,self).__init__(*args, **kwargs)
#        self.fields = patient


class PatientMedicalForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('height','weight','insuranceNum','doctor','hospital','bloodType', 'emergencyContactFirst', 'emergencyContactLast', 'emergencyContactEmail', 'emergencyContactPhone',)
        exclude = ['admissionStatus']

#    def __init__(self, patient, *args, **kwargs):
#        super(PatientProfileForm,self).__init__(*args, **kwargs)
#        self.fields = patient

class ModProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
            'birthday',
            'houseNumber',
            'street',
            'town',
            'state',
            'zip',

        )

class ModEmergencyContactForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = (
            'emergencyContactFirst',
            'emergencyContactLast',
            'emergencyContactEmail',
            'emergencyContactPhone',
        )

class ModMedicalForm(forms.ModelForm):
    class Meta:
        model=PatientProfile
        fields=(
            'height',
            'weight',
            'insuranceNum',
            'bloodType',
        )