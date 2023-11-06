import recordlinkage as rl
import pandas as pd
import requests
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

    #############################################
    email = "fitsumgetu88@gmail.com"
    pwd = "@Admin2020"
    URL = f"https://account.qa.addissystems.et/account/sign-in/{email}/{pwd}"
    data = requests.post(URL)
    print('#############################################')
    print(data.json()['token'])
    print('#############################################')
    #############################################
        # Getting reference data
    users = ReferenceData.objects.all().values()
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
        
        return {
            'first_name':first_name,
            'middle_name':middle_name,
            'last_name':last_name, 
            'email':email,
            'phone':phone,
            'address':address,
            'location':location, 
            'birth_date':birth_date,
            'gender':gender,
        }
    
    def matching_data(self, processed_data):
        # Getting reference data
        users = ReferenceData.objects.all().values()
        
        # Process data into a DataFrame
        reference_data = pd.DataFrame.from_dict(users)
        source_data = pd.DataFrame.from_dict([processed_data])

        # Indexing Records
        indexer = rl.Index()
        indexer.full()
        pairs = indexer.index(reference_data, source_data)
        # print(pairs)

        # Define the comparison step
        compare = rl.Compare()
        compare.exact("first_name", "first_name", label="first_name")
        compare.exact("middle_name", "middle_name", label="middle_name")
        compare.exact("last_name", "last_name", label="last_name")
        compare.exact("email", "email", label="email")
        compare.exact('phone', 'phone', label='phone')
        compare.string('address', 'address', method='jarowinkler', threshold=0.85, label='address')
        compare.exact("birth_date", "birth_date", label="birth_date")
        compare.string("gender", "gender", label="gender")
        compare.string("location", "location", label="location")
        features = compare.compute(pairs, reference_data, source_data)
        
        # Classification step
        matches = features[features.sum(axis=1) > 7]
        print('#################################')
        print(len(matches))
        print(features)
        print('#################################')
        return len(matches)

    def form_valid(self, form: SourceDataForm):
        processed_data = self.process_data(form.cleaned_data)
        self.matching_data(processed_data) # Requesting for matching
        # processed_data.save()
        form = self.form_class()
        # Redirect to a success page or another view
        return redirect(self.success_url)
        # return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm):
        return render(self.request, self.template_name, {'form': form})
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()  # Create a new instance of the form
        return render(request, self.template_name, {'form': form})