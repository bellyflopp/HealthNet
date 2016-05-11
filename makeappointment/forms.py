from django import forms
from django.contrib.auth.models import User, Group
from HealthNet.models import PatientProfile, DoctorProfile, Hospital


class HospitalForm(forms.ModelForm):
    hospital=forms.ModelChoiceField(queryset=Hospital.objects.all())
    class Meta:
        model = Hospital
        fields = ()


