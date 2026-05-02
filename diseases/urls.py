from django.urls import path
from . import views

app_name = 'diseases'

urlpatterns = [
    path('', views.disease_detection, name='detection'),
]
