from django.urls import path

from .views import *


urlpatterns = [
    path('', log_in),
    path('courses/', courses),
    path('logout/', log_out),
    path('courses/<int:pk>/', course),
    path('courses/<int:pk>/<int:stu_id>/', course),
    path('grade/<int:course_id>/<int:stu_id>/', grade),
    path('checkuser/', check_user),
]