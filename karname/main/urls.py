from django.urls import path

from .views import *


urlpatterns = [
    path('', log_in),
    path('grades/', grades),
    path('logout/', log_out),
    path('setGrade/', set_grade),
]