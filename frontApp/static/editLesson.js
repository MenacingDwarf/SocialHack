// Добавление новой карточки или колонки
// Во всех функциях входной параметр elem - кнопка, к которой прикреплена эта функция

// Начать добавление карточки
// Создаёт поле ввода текта новой карточки и кнопки добавления и отмены
// Функция прикрепляется к кнопке внизу колонки
var start_adding_card = function(elem) {
  var input = document.createElement('textarea');
  input.className = "card";
  input.setAttribute("placeholder","Введите название");
  input.onkeydown = pressEnter;
  elem.parentNode.children[1].appendChild(input).focus();

  input = document.createElement('textarea');
  input.className = "card";
  input.setAttribute("placeholder","Введите ссылку");
  input.onkeydown = pressEnter;
  elem.parentNode.children[1].appendChild(input);

  elem.parentNode.replaceChild(make_buttons("Добавить", "add_card(this)", "stop_adding_card(this)"),elem);

  input.scrollIntoView();
}

// Добавить карту
// Добавляет в конец текущей колонки новую карточку
// Функция прикрепляется к кнопке "Добавить карточку"
var add_card = function(elem) {
	var textareas = elem.parentNode.parentNode.children[1].querySelectorAll('textarea.card');
	var card = document.createElement('div');
	card.className = "card";
	card.innerHTML = textareas[0].value;
    card.setAttribute("data-link", textareas[1].value);
    card.setAttribute("onclick", "sendTask(this)");
	var link = document.createElement('div');
	link.setAttribute("hidden","hidden");
	link.innerHTML = textareas[1].value;

	card.appendChild(link);
	sendChanges(textareas[0].value,textareas[1].value,card);
	replace_buttons(elem,"start_adding_card(this)","Добавить");
	textareas[0].parentNode.removeChild(textareas[0]);
	textareas[1].parentNode.replaceChild(card,textareas[1]);
}

// Отмена добавления
// Отменяет добавление новой карточки
// Функция прикрепляется к крестику
var stop_adding_card = function(elem) {
	cards = elem.parentNode.parentNode.children[1];
	cards.removeChild(cards.querySelectorAll('textarea.card')[0]);
	replace_buttons(elem,"start_adding_card(this)","Добавить");
};



// Вспомогательные функции

// Заменяет кнопки, в состав которых входит elem на кнопку добавление с текстом text и прикреплённой к ней функцией func
var replace_buttons = function(elem,func,text) {
  var add = document.createElement('div');
  add.className = "add-card";
  add.setAttribute("onclick",func);
  add.innerHTML = "<div class=\"plus\"></div>"+text;

  elem.parentNode.parentNode.replaceChild(add,elem.parentNode);
}

// Генерирует объект, включающий в себя две кнопки:
// 1. кнопку добавления с текстом text и функцией клика add_function
// 2. кнопку отмены с функцией клика close_function
var make_buttons = function(text,add_function,close_function) {
  var buttons = document.createElement('div');
  var add = document.createElement('div');
  add.className = "add-card-button";
  add.innerHTML = text;
  add.setAttribute("onclick",add_function);

  var close = document.createElement('div');
  close.className = "close";
  close.setAttribute("onclick", close_function);
  var cross = document.createElement('div');
  cross.className = "cross";

  close.appendChild(cross);
  buttons.appendChild(add);
  buttons.appendChild(close);

  return buttons;
}

function printMe(elem) {
    console.log(elem.getAttribute('data-id'));
}

function sendChanges(present_name,present_link,card) {
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
    console.log(present_name);
  var xhr = new XMLHttpRequest();
  var body = "present_name=" + encodeURIComponent(present_name) +
             "&present_url=" + encodeURIComponent(present_link);
  xhr.open("POST", 'update/present/', true);

  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrftoken);

  xhr.onreadystatechange = function() {
	    card.setAttribute('data-id', JSON.parse(this.responseText).id);
	};

  xhr.send(body);
}

function sendTask(card) {
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
  var body = "activity_id=" + encodeURIComponent(card.getAttribute("data-id"));
  xhr.open("POST", '/add', true);

  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader("X-CSRFToken", csrftoken);

  xhr.send(body);
}

// Обработка нажатия клавиши ентер при вводе текста в текстовое поле
function pressEnter(e) {
  if (e.keyCode == 13) {
    e.target.parentNode.parentNode.querySelectorAll('.add-card-button')[0].click();
  }
}
