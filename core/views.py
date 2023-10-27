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
    # context_object_name = ''  Default name is 'form'

    def form_valid(self, form: BaseModelForm):
        
        # Data processing logic goes here...

        return super().form_valid(form)

