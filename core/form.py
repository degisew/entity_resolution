from django import forms
from .models import SourceData

class SourceDataForm(forms.ModelForm):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        ('male', MALE),
        ('female', FEMALE)
    ]
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=GENDER_CHOICES
    )
    birth_date = forms.DateField(label='Birth Date', widget=forms.DateInput(
        attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
    ))
    class Meta:
        model = SourceData
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'email', 'phone', 'address', 'location', 'birth_date']
        