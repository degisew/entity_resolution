import recordlinkage as rl
import pandas as pd
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
    users = ReferenceData.objects.all().values()
    print('#################################')
    print(users)
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
    
    def matching_data(self, processed_data):
        # Getting reference data
        users = ReferenceData.objects.all().values()
        print('#################################')
        print(users)
        print('#################################')
        
        # Process data into a DataFrame
        reference_data = pd.DataFrame(users)
        source_data = pd.DataFrame([processed_data])

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
        compare.string('address', 'address', method='jarowinkler', threshold=0.85)
        compare.exact("birth_date", "date_of_birth", label="date_of_birth")
        compare.string("gender", "gender", label="gender")
        compare.string("location", "location", label="state")
        features = compare.compute(pairs, reference_data, processed_data)
        
        # Classification step
        matches = features[features.sum(axis=1) > 3]
        print('&&&&&&&&&&&&&&&&&', len(matches), '&&&&&&&&&&&&&&&&&',)
        return len(matches)

    def form_valid(self, form: SourceDataForm):
        processed_data = self.process_data(form.cleaned_data)
        self.matching_data(processed_data) # Requesting for matching
        print('ppppppppppppppppppppppppp', processed_data)
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