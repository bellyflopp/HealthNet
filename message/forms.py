from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from HealthNet.models import Message
from django.contrib.auth.models import User


class MessageForm(forms.ModelForm, forms.Form):
    Username=forms.CharField()

    class Meta:
        model = Message
        fields = ('body',)

    def getUserKey(self):
        userStr=self.cleaned_data['Username']
        if not User.objects.filter(username=userStr).exists():
            msg="User does not exist"
            self.add_error('Username', msg)
            return 0
        else:
            return User.objects.get(username=userStr)





