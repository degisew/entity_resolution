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
    # cleaned_data = "  abcjw:, .@! EiwYQA                                "
    # first_name = re.sub('[\W_]+', '', cleaned_data.lower())
    # print("##########################",first_name,"##########################")

    # context_object_name = ''  Default name is 'form'

    def process_data(self, cleaned_data):
        first_name = re.sub('[\W_]+', '',cleaned_data['first_name'].strip().lower())
        middle_name = re.sub('[\W_]+', '',cleaned_data['middle_name'].strip().lower())
        last_name = re.sub('[\W_]+', '',cleaned_data['last_name'].strip().lower())
        email = re.sub('[\W_]+', '',cleaned_data['email'].strip().lower())
        phone = re.sub('[\d_]+', '',cleaned_data['phone'].strip())
        location = re.sub('[\W_]+', '',cleaned_data['location'].strip().lower())
        address = re.sub('[\W_]+', '',cleaned_data['address'].strip().lower())
        birth_date = re.sub('[\W_]+', '',cleaned_data['birth_date'].strip().lower())
        gender = re.sub('[\W_]+', '',cleaned_data['gender'].strip().lower())


    def form_valid(self, form: BaseModelForm):
        
        # Data processing logic goes here...
        return super().form_valid(form)

