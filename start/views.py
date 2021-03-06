from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from database.models import Teacher, Course, Student, StudentCourse, Lesson, DepartmentCourse, Department, Task, \
    Activity, Answer
import pusher
import json
from django.http import JsonResponse


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
        active_lectures = []
        for i in list(courses):
            courses_name.append(i.course.title)
            lectures.append(Lesson.objects.all().filter(course=i.course))
            active_lectures += Lesson.objects.all().filter(course=i.course, is_active=True)

        courses_name = json.dumps(courses_name)
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

        new = []
        for i in dep:
            new.append({
                "course_id": i,
                "predisposition": dep[i]
            })
        dep = json.dumps(new)


        # --------------------------------------------------------------
        return render(request, 'frontApp/studentProfile.html',
                      {'student': student, 'courses': data, 'titles': courses_name, 'lessons': lectures, 'dep': dep,
                       'active': active_lectures})
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
            return render(request, 'frontApp/logPage.html', {'message': 'Неверный логин или пароль'})

    return render(request, 'frontApp/logPage.html')


def push(request, id):
    user = Student.objects.get(user=User.objects.get(id=request.session['_auth_user_id']))
    lesson = Lesson.objects.get(id=id)
    task = Task.objects.get(activity=lesson.current_activity)

    if task.type == 1:
        ref = task.content
        print(ref)
        return render(request, 'frontApp/watchLessonPage.html',
                      {"student": user, "lesson": lesson, "activity": {"message": ref}})
    else:
        question = task.content
        options = list(Answer.objects.all().filter(task=task).values())
        print(options)
        for opt in options:
            opt['correct'] = "True"
        return render(request, 'frontApp/watchLessonPage.html',
                      {'student': user, 'lesson': lesson,
                       'activity': {'question': question, 'options': options}})


def add(request):
    pusher_client = pusher.Pusher(
        app_id='781363',
        key='5a31817a77c426ac84db',
        secret='f31c9e17a3b6bb3e1490',
        cluster='eu',
        ssl=True
    )
    activity = Activity.objects.get(id=request.POST['activity_id'])
    task = Task.objects.get(activity=activity)
    activity.lesson.current_activity = activity
    activity.lesson.save()

    if task.type == 1:
        ref = task.content
        print(ref)
        pusher_client.trigger('my-channel', 'my-event', {'message': ref})
    else:
        question = task.content
        options = Answer.objects.all().filter(task=task)
        pusher_client.trigger('my-channel', 'my-event', {'question': question, 'options': list(options.values())})

    return redirect('/push/1')


def out(request):
    logout(request)
    return redirect('/')


def option(request):
    obj = Answer.objects.get(id=request.POST['answer'])
    obj.students.add(Student.objects.get(id=request.session['_auth_user_id']))
    return redirect('/push/{}'.format(request.POST['lesson']))


def statistic(request, id):
    options = list(Answer.objects.all().filter(task=Task.objects.get(activity=Activity.objects.get(id=id))))
    print(options)
    d = []
    for i in options:
        d.append({"answer": i.text, "litres": len(list(i.students.all()))})
    print(d)

    return JsonResponse({"data": d})


def activate(request):
    lesson = Lesson.objects.get(id=request.POST['id'])
    if lesson.is_active == True:
        lesson.is_active = False
    else:
        lesson.is_active = True
    lesson.save()
    return JsonResponse({'is_active': lesson.is_active})
