from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # This will map the root URL to the index view
    path('fetch-data/', views.fetch_data, name='fetch_data'),
]
