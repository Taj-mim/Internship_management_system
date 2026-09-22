from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class StudentRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = User.Role.STUDENT

        if commit:
            user.save()

        return user


class CompanyRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    organization_name = forms.CharField(
        max_length=255
    )

    website = forms.URLField(
        required=False
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "organization_name",
            "website",
            "password1",
            "password2",
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = User.Role.COMPANY

        if commit:
            user.save()

        return user