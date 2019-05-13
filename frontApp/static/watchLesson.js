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

function displayActivity(data) {
    if (document.getElementById("content")) {
        document.getElementById("content").parentNode.removeChild(document.getElementById("content"));
    }

    var content = document.createElement('div');
    content.id = "content";

    if (data.message) {
        var edit_save = document.createElement("img");
        edit_save.style = "margin-top: 20px; max-width: 100%";
        edit_save.src = data.message;
        content.appendChild(edit_save);
    } else {

        if (data.question !== undefined) {
            var q = document.createElement('h3');
            q.innerHTML = data.question;
            content.appendChild(q);
        }

        var form = document.createElement('form');
        form.setAttribute('action', '/option/');
        form.setAttribute('method', 'POST');

        var csrf = document.createElement('input');
        csrf.setAttribute('type', 'hidden');
        csrf.name = 'csrfmiddlewaretoken';
        csrf.value = csrftoken;
        form.appendChild(csrf);

        var lesson = document.createElement('input');
        lesson.value = document.getElementById("lesson").getAttribute("data-id");
        lesson.name = 'lesson';
        lesson.setAttribute("hidden", "hidden");
        form.appendChild(lesson);
        data.options.forEach((item) => {
            var option = document.createElement("input");
            option.id = item.id;
            option.setAttribute("type", "radio");
            option.value = item.id;
            option.name = "answer";

            var label = document.createElement("label");
            label.setAttribute("for", item.id);
            label.innerHTML = item.text;

            var input = document.createElement("p");
            input.appendChild(option);
            input.appendChild(label);
            form.appendChild(input);
        });

        var button = document.createElement('button');
        button.setAttribute('type', 'submit');
        button.className = "btn btn-primary";
        button.innerHTML = "Отправить";
        form.appendChild(button);
        content.appendChild(form);
    }
    document.getElementById("lection").appendChild(content);
}

var content = document.getElementById("content");
if (content) {
    var data = JSON.parse(document.getElementById("content").innerHTML.replace(new RegExp('\'', 'g'),'\"'));
    displayActivity(data);
}



var csrftoken = getCookie('csrftoken');

// Enable pusher logging - don't include this in production
Pusher.logToConsole = true;

var pusher = new Pusher('5a31817a77c426ac84db', {
    cluster: 'eu',
    forceTLS: true
});

var channel = pusher.subscribe('my-channel');

channel.bind('my-event', function (data) {
    displayActivity(data);
});
