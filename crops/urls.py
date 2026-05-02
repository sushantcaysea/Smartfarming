from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crop_recommendation, name='recommendation'),
]
