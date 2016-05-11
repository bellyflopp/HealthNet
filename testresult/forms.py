from django import forms
from HealthNet.models import TestModel

class testForm(forms.ModelForm):
    class Meta:
        model=TestModel
        fields = (
            'testName',
            'result',
            'notes',
        )
