from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from .models import *

def get_user(request):
    try:
        user_id = request.session['studentID']
        user = Student.objects.get(id=user_id)
    except:
        user = None
    
    return user

def log_in(request):
    user = get_user(request)
    if user:
        return redirect('/grades/')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        default_method = request.POST.get('default', None)
        if default_method:
            try:
                user = Student.objects.get(username=username, password=password)
                request.session['studentID'] = user.id
                request.session.set_expiry(None)
            except:
                return redirect('/')

            return redirect('/grades/')     
        else:
            data = {
                'username': username,
                'password': password,
            }
            res = requests.post("https://moodle25.pythonanywhere.com/checkuser/", data=data)
            res_data = json.loads(res.text)
            if res_data['valid']:
                try:
                    user = Student.objects.get(student_number=username)
                    request.session['studentID'] = user.id
                    request.session.set_expiry(None)
                    return redirect('/grades/')     
                except:
                    return redirect('/')
            else:
                return redirect('/')

    else:
        return render(request, 'login.html')


def log_out(request):
	try:
		del request.session['studentID']
	except:
		pass

	return redirect("/")


def grades(request):
    user = get_user(request)
    if not user:
        return redirect('/')

    grades = user.grades.all()

    return render(request, 'grades.html', {
        'user': user,
        'grades': grades,
    })
    
@csrf_exempt
def set_grade(request):
    auth_token = request.POST.get('token', '')
    if auth_token != 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9':
        return JsonResponse({'message': 'AUTH FAILED'})
    student_number = request.POST.get('student_number')
    course_number = request.POST.get('course_number')
    teacher = request.POST.get('teacher')
    total = request.POST.get('grade')

    course = Course.objects.get(course_number=course_number)
    stu = Student.objects.get(student_number=student_number)
    try:
        grade = Grade.objects.get(course=course, teacher=teacher)
        grades = stu.grades.all()
        if grade in grades:
            grade.total = total
            grade.save()
        else:
            raise Exception()
    except:    
        grade = Grade(
            course=course,
            teacher=teacher,
            total=total
        )
        grade.save()
        stu.grades.add(grade)
        stu.save()
    return JsonResponse({'message': 'DONE'})

