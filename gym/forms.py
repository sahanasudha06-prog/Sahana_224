
from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member

        fields = [
            'name',
            'email',
            'phone',
            'membership_type',
            'joining_date',
            'expiry_date',
            'is_active',
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'expiry_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
