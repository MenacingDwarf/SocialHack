from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from database.models import Teacher, Course, Student, StudentCourse, Lesson, DepartmentCourse, Department, Task, \
    Activity, Answer
import pusher
import json


def home(request):
    if '_auth_user_id' not in request.session.keys():
        return redirect('/log')

    user = User.objects.get(id=request.session['_auth_user_id'])

    if 'st' in user.username:
        student = Student.objects.get(user=user)
        courses = StudentCourse.objects.all().filter(student=student)
        data = json.dumps(list(courses.values()))
        courses_name = []
        lectures = []
        for i in list(courses):
            courses_name.append(i.course.title)
            lectures.append(Lesson.objects.all().filter(course=i.course))

        # --------------------------------------------------------------
        departments = list(Department.objects.all())
        department_course = list(DepartmentCourse.objects.all())
        student_courses = list(StudentCourse.objects.all().filter(student=student))

        dep = {}
        for department in departments:
            n = 0
            dep[department.name] = 0
            for course in student_courses:
                for el in department_course:
                    if el.coef > 0.4:
                        n += 1
                    if el.department.id == department.id and el.course.id == course.id:
                        dep[department.name] += el.coef * course.attendance * course.correctness
            dep[department.name] /= n - 1

        print(dep)
        dep = json.dumps(dep)
        # --------------------------------------------------------------

        return render(request, 'start/student.html',
                      {'courses': data, 'titles': courses_name, 'lessons': lectures, 'dep': dep})
    else:
        teacher = Teacher.objects.get(user=user)
        course = Course.objects.all().filter(tutor=teacher)
        return render(request, 'frontApp/teacherProfile.html', {'teacher': teacher, 'courses': course})


def log(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user'], password=request.POST['pass'])
        if user and user.is_active == True:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'start/log.html', {'message': 'Неверный логин или пароль'})

    return render(request, 'start/log.html')


def push(request, id):
    return render(request, 'start/pusher.html')


def add(request):
    pusher_client = pusher.Pusher(
        app_id='780550',
        key='a26085dc09d59ab89666',
        secret='c6ac4917c6fcca212017',
        cluster='eu',
        ssl=True
    )

    task = Task.objects.get(activity=Activity.objects.get(id=request.POST['activity_id']))

    if task.type == 1:
        ref = task.content
        pusher_client.trigger('my-channel', 'my-event', {'message': ref})
    else:
        question = task.content
        options = Answer.objects.all(task=task)
        pusher_client.trigger('my-channel', 'my-event', {'question': question, 'options': list(options)})

    return redirect('/push')


def out(request):
    logout(request)
    return redirect('/')
