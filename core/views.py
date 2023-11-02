
import re
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.views import View
from .models import ReferenceData, SourceData
from .form import SourceDataForm


class HomeView(View):
    def get(self, request):
        return HttpResponse('Home')


class SourceDataView(CreateView):
    model = SourceData
    form_class = SourceDataForm
    template_name = 'core/form.html'
    success_url = 'home'

    # Getting reference data
    users = ReferenceData.objects.all()
    print('#################################')
    print([ user.first_name for user in users])
    print('#################################')

    def process_data(self, cleaned_data):
        first_name = re.sub(
            r'[\W\d_\\\.@#$%^&*~]+', '', cleaned_data['first_name'].strip().lower())
        middle_name = re.sub(
            r'[\W\d_\\\.@#$%^&*~]+', '', cleaned_data['middle_name'].strip().lower())
        last_name = re.sub(
            r'[\W\d_\\\.@#$%^&*~]+', '', cleaned_data['last_name'].strip().lower())
        email = cleaned_data[r'email'].strip().lower()
        phone = re.sub(r'[\D_]+', '', cleaned_data['phone'].strip())
        location = re.sub(r'[\W\d_\\\.@#$%^&*~]+', '',
                          cleaned_data['location'].strip().lower())
        address = re.sub(r'[\W\d_,[\]./#]+', '',
                         cleaned_data['address'].strip().lower())
        birth_date = re.sub(r'[a-zA-Z_\.@#$%^&*~]', '',
                            str(cleaned_data['birth_date']))
        gender = re.sub(r'[\d_\\\.@#$%^&*~]+', '',
                        cleaned_data['gender'].strip().lower())

        return SourceData(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name, 
            phone=phone,
            email=email,
            location=location, 
            address=address,
            gender=gender,
            birth_date=birth_date,
        )
    
    def matching_data(self):
        # Add a logic here
        pass
    

    def form_valid(self, form: SourceDataForm):
        processed_data = self.process_data(form.cleaned_data)
        print(processed_data)
        processed_data.save()
        form = self.form_class()
        # Redirect to a success page or another view
        return redirect(self.success_url)
        # return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm):
        return render(self.request, self.template_name, {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()  # Create a new instance of the form
        return render(request, self.template_name, {'form': form})