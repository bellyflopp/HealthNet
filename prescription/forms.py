from django import forms
from HealthNet.models import Prescription


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = (
            'name',
            'note',
        )
