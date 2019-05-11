function startAddingLesson(elem) {
	var lessons = elem.parentNode;
	var lesson = document.createElement('div');
	lesson.className = "lesson-card card";
	var input = document.createElement('textarea');
	input.className = "card";
	input.setAttribute("placeholder","Введите название лекции");

	var add = document.createElement('div');
  	add.className = "add-card-button";
  	add.innerHTML = "Добавить лекцию";
  	add.setAttribute("onclick",'addLesson(this)');

  	lesson.appendChild(input);
  	lesson.appendChild(add);

  	lessons.replaceChild(lesson,elem);
  	lessons.querySelectorAll('textarea')[0].focus();
}

function addLesson(elem) {
    var lesson = createLesson(0,elem.parentNode.querySelectorAll('textarea')[0].value,elem.parentNode);
	sendChanges(lesson);
	replaceLesson(elem.parentNode);
}
function createLesson(id,title,next) {
	var lesson = document.createElement('a');
	lesson.className = "card lesson-card";
	lesson.setAttribute('href','id');
	lesson.id = id;
	lesson.innerHTML = title;
	lesson = next.parentNode.insertBefore(lesson,next);
	return lesson;
}

function replaceLesson(elem) {
	var lesson = document.createElement('div');
	lesson.className = 'card new-lesson';
	lesson.innerHTML = 'Новая лекция';
	lesson.setAttribute('onclick','startAddingLesson(this)');
	elem.parentNode.replaceChild(lesson,elem);
}

function sendChanges(lesson) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
	var xhr = new XMLHttpRequest();

	var body = 'lesson_name=' + encodeURIComponent(lesson.innerHTML);

	xhr.open("POST", '/courses/update/'+
        document.getElementById("course_id").innerHTML+'/', true);
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.setRequestHeader("X-CSRFToken", csrftoken)

	xhr.onreadystatechange = function() {
	    console.log(this.responseText);
	    lesson.setAttribute('href', JSON.parse(this.responseText).id);
	};

	xhr.send(body);
}