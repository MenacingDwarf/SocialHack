from django.shortcuts import render


def hello(request):
    return render(request, 'frontApp/teacherProfile.html', {"teacher": {"name": "Сергей", "second_name": "Погожев"},
                                                            "courses": [{"title": "first"},
                                                                        {"title": "second"},
                                                                        {"title": "third"}]})
