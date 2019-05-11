from django.shortcuts import render,redirect
from database.models import Course, Lesson, Activity
from django.http import JsonResponse


# Create your views here.
def courses(request, id):
    lessons = Lesson.objects.all().filter(course=id)

    teacher = Course.object.get(id=id).tutor


    return render(request, 'frontApp/lessonsPage.html', {'lessons': lessons, 'id': id, 'teacher': teacher})


def update(request,id):
    if request.method == 'POST':
        lesson_name = request.POST['lesson_name']
    obj = Lesson(title = lesson_name,course = Course.objects.get(id=id))
    obj.save()
    return JsonResponse({"id": obj.id})

def lesson(request, id_course, id_lesson):
    lessons = Activity.objects.all().filter(lesson=id_lesson)


    return render(request, 'task/tasks.html', {'lessons': lessons})
