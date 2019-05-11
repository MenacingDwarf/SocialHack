from django.shortcuts import render,redirect
from database.models import Course, Lesson, Activity

# Create your views here.
def courses(request, id):
    lessons = Lesson.objects.all().filter(course=id)


    return render(request, 'task/lessons.html', {'lessons': lessons, 'id': id})

def update(request,id):
    if request.method == 'POST':
        lesson_name = request.POST['lesson_name']

    obj = Lesson(title = lesson_name,course = Course.objects.get(id=id))
    obj.save()
    return redirect('/courses/{}'.format(id))

def lesson(request, id_course, id_lesson):
    lessons = Activity.objects.all().filter(lesson=id_lesson)


    return render(request, 'task/lessons.html', {'lessons': lessons})