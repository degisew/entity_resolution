from django.urls import path
from .views import SourceDataView, HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('create/', SourceDataView.as_view(), name='create-data')
]