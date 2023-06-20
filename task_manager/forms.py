from django import forms
from django.forms import PasswordInput
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Worker


class WorkerCreateForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput())

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "position"
        ]


class WorkerUpdateForm(forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("last_name", "position",)
