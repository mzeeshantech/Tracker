from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get-breaker-detail/', views.get_breaker_detail, name='get_breaker_detail'),
    path('get_paginated_data/', views.get_paginated_data, name='get_paginated_data'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]
