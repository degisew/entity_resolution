import re
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import CreateView
from django.views import View
from .models import SourceData 
from .form import SourceDataForm

class HomeView(View):
    def get(self, request):
        return HttpResponse('Home')

class SourceDataView(CreateView):
    model = SourceData
    form_class = SourceDataForm
    template_name = 'core/form.html'
    success_url = 'home'

    
    def process_data(self, cleaned_data):
        first_name = re.sub(r'[\W_]+', '',cleaned_data['first_name'].strip().lower())
        middle_name = re.sub(r'[\W_]+', '',cleaned_data['middle_name'].strip().lower())
        last_name = re.sub(r'[\W_]+', '',cleaned_data['last_name'].strip().lower())
        email = cleaned_data[r'email'].strip().lower()
        phone = re.sub(r'[\D_]+', '',cleaned_data['phone'].strip())
        location = re.sub(r'[\W_]+', '',cleaned_data['location'].strip().lower())
        address = re.sub(r'[\W\d_,[\]./#]+', '',cleaned_data['address'].strip().lower())
        birth_date = re.sub(r'[a-zA-Z_\.@#$%^&*~]', '',cleaned_data['birth_date'].strip().lower())
        gender = re.sub(r'[\d_\\\.@#$%^&*~]+', '',cleaned_data['gender'].strip().lower())


    def form_valid(self, form: BaseModelForm):
        # Data processing logic goes here...
        return super().form_valid(form)

