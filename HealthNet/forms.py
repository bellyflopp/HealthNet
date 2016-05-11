from django import forms
from HealthNet.models import Appointment, FileUpload, DoctorProfile, Hospital, Visit

'''
Form for creating an appointment as a patient
'''
class AppointmentPatientForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = (
            'doctor',
            'date',
            'time',
        )

'''
Form for creating an appointment as a doctor
'''
class AppointmentDoctorForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = (
            'patient',
            'date',
            'time',
        )

'''
Form for creating an appointment as a nurse
'''
class AppointmentNurseForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = (
            'patient',
            'doctor',
            'date',
            'time',
        )

class uploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = (
            'file',
        )

class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = (
            'reason',
        )