from django import forms

from accounts.models import Apply


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Apply

        fields = [
            'full_name',
            'email',
            'phone',
            'resume_file',
            'cover_letter_file',
        ]

        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your full name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your email'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your phone number'
                }
            ),

            'resume_file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'cover_letter_file': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control' 
                }
            ),
        }
