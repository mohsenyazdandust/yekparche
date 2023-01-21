import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect

from .models import *

def get_user(request):
    try:
        user_id = request.session['StuID']
        user = Student.objects.get(id=user_id)
        user_type = 's'
    except:
        try:
            user_id = request.session['TrID']
            user = Teacher.objects.get(id=user_id)
            user_type = 't'
        except:
            user = None
            user_type = None
    
    return [user, user_type]

def log_in(request):
    user = get_user(request)
    if user[0]:
        return redirect('/courses/')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = Student.objects.get(username=username, password=password)
            request.session['StuID'] = user.id
            request.session.set_expiry(None)
        except:
            try:
                user = Teacher.objects.get(username=username, password=password)
                request.session['TrID'] = user.id
                request.session.set_expiry(None)
            except:
                return redirect('/')

        return redirect('/courses/')        
    else:
        return render(request, 'login.html')


def log_out(request):
	try:
		del request.session['StuID']
	except:
		pass
	
	try:
		del request.session['TrID']
	except:
		pass


	return redirect("/")


def courses(request):
    user = get_user(request)
    if not user[0]:
        return redirect('/')

    courses = user[0].courses.all()

    return render(request, 'course.html', {
        'user': user[0],
        'courses': courses,
    })
    

def course(request, pk, stu_id=0):
    user = get_user(request)
    if not user[0]:
        return redirect('/')

    c = Course.objects.get(id=pk)
    students = Student.objects.filter(courses=c)
    grade = None


    if user[1] == 's':
        if not stu_id or stu_id == user[0].id:
            try:
                grade = Grade.objects.get(user=user[0], course=c)
            except:
                pass
        
        return render(request, 'detail-student.html', {
            'user': user[0],
            'course': c,
            'students': students,
            'grade': grade,
        })
    else:
        stu = None
        if stu_id:
            stu = Student.objects.get(id=stu_id)
            try:
                grade = Grade.objects.get(user=stu, course=c)
            except:
                pass

        return render(request, 'detail-teacher.html', {
            'user': user[0],
            'course': c,
            'students': students,
            'grade': grade,
            'student': stu
        })


def grade(request, stu_id, course_id):
    if request.method == 'POST':
        stu = Student.objects.get(id=stu_id)
        c = Course.objects.get(id=course_id)
        mid_term = request.POST.get('mid_term', 0)
        final = request.POST.get('final', 0)
        activities = request.POST.get('activities', 0)
        total = float(mid_term) + float(final) + float(activities)
        try:
            grade = Grade.objects.get(user=stu, course=c)
            grade.mid_term = mid_term
            grade.final = final
            grade.activities = activities
            grade.total = total
        except:
            grade = Grade(
                user=stu,
                course=c,
                mid_term=mid_term,
                final=final,
                activities=activities,
                total=total
            )
        grade.save()

        # SEND REQUEST TO "GOLESTAN"
        teacher = Teacher.objects.filter(courses=c)[0]
        url = 'https://golestan25.pythonanywhere.com/setGrade/'
        data = {
            'student_number': stu.username,
            'course_number': c.course_number,
            'teacher': teacher.name,
            'grade': total,
        }

        requests.post(url, data=data)
        
        return redirect('/courses/{}/{}'.format(c.id, stu.id))
    else:
        return redirect('/')

@csrf_exempt
def check_user(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    try:
        user = Student.objects.get(username=username, password=password)
        return JsonResponse({'valid': True})
    except:
        return JsonResponse({'valid': False})
