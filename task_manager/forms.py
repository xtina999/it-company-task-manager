from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.forms import PasswordInput, DateInput
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Worker, Task


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


class WorkerAccountsUpdateForm(forms.ModelForm):

    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("username", "email", "position", "first_name", "last_name",)


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "is_completed",
            "priority",
            "task_type",
            "assignees"
        ]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
    )