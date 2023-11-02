from typing import Any
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
        
    
    # def save(self, commit: bool =True):
    #     instance = super(SourceDataForm, self).save(commit=False)
    #     instance.first_name = self.cleaned_data.get('first_name')
    #     instance.middle_name = self.cleaned_data.get('middle_name')
    #     instance.last_name = self.cleaned_data.get('last_name')
    #     instance.phone = self.cleaned_data.get('phone')
    #     instance.email = self.cleaned_data.get('email')
    #     instance.location = self.cleaned_data.get('location')
    #     instance.gender = self.cleaned_data.get('gender')
    #     instance.address = self.cleaned_data.get('address')
    #     instance.birth_date = self.cleaned_data.get('birth_date')
    #     if commit:
    #         instance.save()
    #     return instance