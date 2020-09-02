
function onLoad() {
    var location_Url = window.location.href;
    // funCss(location_Url);
    if(location_Url) {
        var text_msg = "yes";
        var question = "welcome";
        funChatbox(text_msg, question);
    }
}

function funCss(location_Url) {
    var Url = "http://18.221.57.172:8000/client-css";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', Url, true);
    var data = JSON.stringify({
        "location_Url": location_Url
    });
    xhr.send(data);
    xhr.onreadystatechange = processRequest;
    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {

            var ajaxResponse = JSON.parse(xhr.responseText);

            console.log(ajaxResponse);
        }
    }
}

function funChatbox(text_msgs, ques_msg) {
    console.log(text_msgs)
    console.log(ques_msg)

    var textmsg;
    if (text_msgs == '') {
        textmsg = document.getElementById("txtmsgid").value;
    } else {
        textmsg = text_msgs;
    }

    var question;
    if (ques_msg == '') {
        question = document.getElementById("resquestion").innerHTML;
    } else {
        question = ques_msg;
    }

    console.log(document.getElementById("resquestion").innerHTML);

    /* var question;
    if (ques_msg != 'welcome') {
        question = document.getElementById("resquestion").innerHTML;
    } else {
        question = ques_msg;
    } */

    var Url = "http://18.221.57.172:8000/client-form";
    var xhr = new XMLHttpRequest();
    xhr.open('POST', Url, true);
    var data = JSON.stringify({
        "bot_id": 1,
        "question": question,
        "text": textmsg,
        "ip": "192.168.0.1",
        "sessionId": "3c3a3f6a-7cbc-4b99-b058-1734c842c6ec"
    });
    xhr.send(data);
    xhr.onreadystatechange = processRequest;
    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {

            var ajaxResponse = JSON.parse(xhr.responseText);

            //document.forms["myForm"]["text_msg"].value = "";
            document.getElementById("txtmsgid").value = "";

            console.log(ajaxResponse);

            showResponse(ajaxResponse);
        }
    }
}

function showResponse(ajaxResponse) {
    var responseContainer = document.querySelector('#responseContainer');
    var linebreak = document.createElement("br");

    var newItem = document.createElement('div');
    newItem.className = ('received-chats');

    var newItem1 = document.createElement('div');
    newItem1.className = ('received-chats-img');
    newItem1.innerHTML = ('<img src="imgs/chat_new.png">');
    newItem.appendChild(newItem1);

    var newItem2 = document.createElement('div');
    newItem2.className = ('received-msg');

    var newItem21 = document.createElement('div');
    newItem21.className = ('received-msg-inbox');
    var para = document.createElement('p');
    // document.getElementsByClassName("received-msg-inbox").style.color = "blue";

    var span = document.createElement('span');
    span.innerHTML = ajaxResponse[0].question;
    //console.log(ajaxResponse[0].question);
    span.appendChild(linebreak);

    var sug_answers = ajaxResponse[0].suggested_answers;
    for (var x = 0; x < sug_answers.length; x++) {
        var newbtn = document.createElement('input');
        newbtn.type = 'button';
        newbtn.value = sug_answers[x].payload;
        newbtn.innerHTML = sug_answers[x].title;
        //console.log(sug_answers[x].payload);
        newbtn.addEventListener("click", function (event) {
            var btnValue = event.target.value;

            var newItem_oc = document.createElement('div');
            newItem_oc.className = ('outgoing-chats');

            var newItem_oc1 = document.createElement('div');
            newItem_oc1.className = ('outgoing-chats-msg');
            var para_oc = document.createElement('p');

            var span_oc = document.createElement('span');
            span_oc.innerHTML = btnValue;
            para_oc.appendChild(span_oc);
            newItem_oc1.appendChild(para_oc);
            newItem_oc.appendChild(newItem_oc1);

            var newItem_oc2 = document.createElement('div');
            newItem_oc2.className = ('outgoing-chats-img');
            newItem_oc2.innerHTML = ('<img src="imgs/user.png">');
            newItem_oc.appendChild(newItem_oc2);

            newItem_oc.scrollTop = newItem_oc.scrollHeight;

            responseContainer.appendChild(newItem_oc);
            responseContainer.scrollTop = responseContainer.scrollHeight;

            funChatbox(btnValue, ajaxResponse[0].question);

        });
        span.appendChild(newbtn);
    }

    para.appendChild(span);

    newItem21.appendChild(para);
    newItem2.appendChild(newItem21);
    newItem.appendChild(newItem2);

    newItem.scrollTop = newItem.scrollHeight;

    document.getElementById("resquestion").innerHTML = ajaxResponse[0].question;

    responseContainer.appendChild(newItem);
    responseContainer.scrollTop = responseContainer.scrollHeight;

    if (ajaxResponse[0].answer_type == 'TEXT') {
        document.getElementById("bolForm").style.display = "block";
    } else {
        document.getElementById("bolForm").style.display = "none";
    }


    // if (ajaxResponse[0].is_last_question == false) {
    //     document.getElementById("bolChat").style.pointerEvents = "auto";
    // } else {
    //     document.getElementById("bolChat").style.pointerEvents = "none";
    // }
}




function doit_onkeypress(event) {
    if (event.keyCode == 13 || event.which == 13) {
        funTextMsg();
    }
}

function funTextMsg() {

    if (document.getElementById("txtmsgid").value != '') {
        textmsg = document.getElementById("txtmsgid").value;

        console.log(document.getElementById("resquestion").innerHTML);
        var responseContainer = document.querySelector('#responseContainer');

        var newItem_oc = document.createElement('div');
        newItem_oc.className = ('outgoing-chats');

        var newItem_oc1 = document.createElement('div');
        newItem_oc1.className = ('outgoing-chats-msg');
        var para_oc = document.createElement('p');

        var span_oc = document.createElement('span');
        //span_oc.innerHTML = document.forms["myForm"]["text_msg"].value;
        span_oc.innerHTML = document.getElementById("txtmsgid").value;
        para_oc.appendChild(span_oc);
        newItem_oc1.appendChild(para_oc);
        newItem_oc.appendChild(newItem_oc1);

        var newItem_oc2 = document.createElement('div');
        newItem_oc2.className = ('outgoing-chats-img');
        newItem_oc2.innerHTML = ('<img src="imgs/user.png">');
        newItem_oc.appendChild(newItem_oc2);

        newItem_oc.scrollTop = newItem_oc.scrollHeight;

        responseContainer.appendChild(newItem_oc);
        responseContainer.scrollTop = responseContainer.scrollHeight;

        funChatbox('', '');
    } else {
        alert("Please enter your Text Message.")
    }
}