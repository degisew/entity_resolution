from django.forms import ModelForm
from .models import SourceData

class SourceDataForm(ModelForm):
    class Meta:
        model = SourceData
        fields = ['first_name', 'middle_name', 'last_name', 'gender', 'email', 'phone', 'address', 'location', 'birth_date']