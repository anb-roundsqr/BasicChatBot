var sessionIdGlobal = '';

function onLoad() {
    var location_Url = window.location.href;
    funCss(location_Url);

}

async function funCss(location_Url) {
    var Url = "https://api.chatbotdev.roundsqr.net/bot-properties?source_url=";
    var params = location_Url;

    try {
        let r = await fetch(Url + params, { method: "GET" })
            .then(response => response.text())
            .then(data =>
                response = JSON.parse(data));
        console.log(response)

        if (response.status == 'success') {
            if (location_Url) {
                var text_msg = "yes";
                var question = "welcome";
                funChatbox(text_msg, question, response, '');
            }
        }
    } catch (e) {
        console.log('Powerbot we have problem...:', e);
    }
}


function funChatbox(text_msgs, ques_msg, response, sessionId) {

    var textmsg;
    sessionIdGlobal = sessionId;

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
    // jQuery.get("https://api.ipdata.co?api-key=test", function (response) {
    //     console.log(response.ip);
    // }, "jsonp");
    // jQuery.getJSON("https://api.ipify.org?format=json",
    //     function (data) {
    //        var ip_sys = data.ip;
    //         console.log(ip_sys)
    //     })

    var ip_sys = jQuery.getJSON("https://api.ipify.org?format=json",
        function (data) {
            ip_sys = data.ip;
            iprotocol(ip_sys)
        })
    function iprotocol(ip_sys) {

        var Url = "https://api.chatbotdev.roundsqr.net/client-form";
        var xhr = new XMLHttpRequest();
        xhr.open('POST', Url, true);
        var data = JSON.stringify({
            "bot_id": 1,
            "location": window.location.href,
            "question": question,
            "text": textmsg,
            "ip": ip_sys,
            "sessionId": sessionId
        });
        xhr.send(data);
        xhr.onreadystatechange = processRequest;
        function processRequest(e) {
            if (xhr.readyState == 4 && xhr.status == 200) {

                var ajaxResponse = JSON.parse(xhr.responseText);
                document.getElementById("txtmsgid").value = "";
                showResponse(ajaxResponse, response);
            }
        }
    }
}

function showResponse(ajaxResponse, response) {
    console.log(response);
    var seconds = new Date().getTime() / 1000;
    console.log(seconds) 
    var css = response.response;
    console.log(css.header_colour)
    var headerBlock = document.getElementById('mydiv');
    headerBlock.style.background = css.header_colour;

    var headerText = document.getElementsByTagName("h4");
    headerText[0].style.color = css.header_colour;
    headerText[0].innerHTML = "Chat with us now!";

    var headerContainer = document.querySelector('#icon');
    // headerContainer.style.backgroundColor = '#ccffff';
    var newIcon = document.createElement('div');
    newIcon.className = ('chats-logo');
    var botLogo = "https://api.chatbotdev.roundsqr.net/" + css.bot_logo;
    console.log(botLogo)
    newIcon.innerHTML = ('<img src= ' + botLogo + '>');
    // newIcon.appendChild(newIcon);
    headerContainer.appendChild(newIcon)

    var responseContainer = document.querySelector('#responseContainer');
    //body background colour
    // responseContainer.style.backgroundColor = css.body_color;

    var linebreak = document.createElement("br");

    var newItem = document.createElement('div');
    newItem.className = ('received-chats');
    //bot div complete element colour
    // newItem.style.backgroundColor = '#ffffff';

    if (ajaxResponse[0].error_msg) {
        var linebreakError = document.createElement("br");

        var newItemError = document.createElement('div');
        newItemError.className = ('received-chats-error');

        var newItem1Error = document.createElement('div');
        newItem1Error.className = ('received-chats-img-error');
        var botImgError = "https://api.chatbotdev.roundsqr.net/" + css.bot_logo;
        console.log(botImgError)
        newItem1Error.innerHTML = ('<img src= ' + botImgError + '>');
        newItemError.appendChild(newItem1Error);

        var newItem2Error = document.createElement('div');
        newItem2Error.className = ('received-msg-error');


        var newItem21Error = document.createElement('div');
        newItem21Error.className = ('received-msg-inbox-error');
        //font color of bot msg
        newItem21Error.style.color = css.chat_bot_font_colour;
        //bot chat bubble backgroundcolor
        newItem21Error.style.backgroundColor = css.bot_bubble_colour;

        var paraError = document.createElement('p');

        var spanError = document.createElement('span');
        spanError.innerHTML = ajaxResponse[0].error_msg;
        spanError.appendChild(linebreakError);
        paraError.appendChild(spanError);

        newItem21Error.appendChild(paraError);
        newItem2Error.appendChild(newItem21Error);
        newItemError.appendChild(newItem2Error);

        newItemError.scrollTop = newItemError.scrollHeight;

        document.getElementById("resquestion").innerHTML = ajaxResponse[0].error_msg;

        responseContainer.appendChild(newItemError);
        responseContainer.scrollTop = responseContainer.scrollHeight;


    }

    var newItem1 = document.createElement('div');
    newItem1.className = ('received-chats-img');
    var botImg = "https://api.chatbotdev.roundsqr.net/" + css.bot_logo;
    console.log(botImg)
    newItem1.innerHTML = ('<img src= ' + botImg + '>');
    newItem.appendChild(newItem1);

    var newItem2 = document.createElement('div');
    newItem2.className = ('received-msg');


    var newItem21 = document.createElement('div');
    newItem21.className = ('received-msg-inbox');
    //font color of bot msg
    newItem21.style.color = css.chat_bot_font_colour;
    //bot chat bubble backgroundcolor
    newItem21.style.backgroundColor = css.bot_bubble_colour;

    var para = document.createElement('p');


    var span = document.createElement('span');
    span.innerHTML = ajaxResponse[0].question;
    span.appendChild(linebreak);

    var sug_answers = ajaxResponse[0].suggested_answers;

    if(ajaxResponse[0].type == 'file') {
        
        for (var x = 0; x < sug_answers.length; x++) {
            var imgItem = document.createElement('div');
            imgItem.className = ('carousel-item');
            var newbtn = document.createElement('IMG');
            newbtn.height = '120'
            newbtn.width = '80'
            // newbtn.type = 'button';
            newbtn.src = "https://api.chatbotdev.roundsqr.net/" + sug_answers[x].payload;
            newbtn.value = sug_answers[x].title;
            newbtn.addEventListener("click", function (event) {
                var btnValue = event.target.value;

                var newItem_oc = document.createElement('div');
                newItem_oc.className = ('outgoing-chats');
                //user chat container background color
                // newItem_oc.style.backgroundColor = '#ccffff';

                var newItem_oc1 = document.createElement('div');
                newItem_oc1.className = ('outgoing-chats-msg');
                var para_oc = document.createElement('p');
                //user chat bubble backgroundcolor
                para_oc.style.backgroundColor = css.user_bubble_colour;
                //user chat text color
                para_oc.style.color = css.chat_user_font_colour;
                

                var span_oc = document.createElement('span');
                span_oc.innerHTML = btnValue;
                para_oc.appendChild(span_oc);
                newItem_oc1.appendChild(para_oc);
                newItem_oc.appendChild(newItem_oc1);

                var newItem_oc2 = document.createElement('div');
                newItem_oc2.className = ('outgoing-chats-img');
                var userImg = "https://api.chatbot.roundsqr.net/" + css.user_logo;
                newItem_oc2.innerHTML = ('<img src= ' + userImg + '>');
                newItem_oc.appendChild(newItem_oc2);

                newItem_oc.scrollTop = newItem_oc.scrollHeight;

                responseContainer.appendChild(newItem_oc);
                responseContainer.scrollTop = responseContainer.scrollHeight;

                funChatbox(btnValue, ajaxResponse[0].question, response, ajaxResponse[0].sessionId);

            });
            span.appendChild(newbtn);
        }
    } else {
        for (var x = 0; x < sug_answers.length; x++) {
            var newbtn = document.createElement('input');
            newbtn.type = 'button';
            newbtn.value = sug_answers[x].title;
            newbtn.innerHTML = sug_answers[x].title;
            newbtn.addEventListener("click", function (event) {
                var btnValue = event.target.value;

                var newItem_oc = document.createElement('div');
                newItem_oc.className = ('outgoing-chats');
                //user chat container background color
                // newItem_oc.style.backgroundColor = '#ccffff';


                var newItem_oc1 = document.createElement('div');
                newItem_oc1.className = ('outgoing-chats-msg');
                var para_oc = document.createElement('p');
                //user chat bubble backgroundcolor
                para_oc.style.backgroundColor = css.user_bubble_colour;
                //user chat text color
                para_oc.style.color = css.chat_user_font_colour;



                var span_oc = document.createElement('span');
                span_oc.innerHTML = btnValue;
                para_oc.appendChild(span_oc);
                newItem_oc1.appendChild(para_oc);
                newItem_oc.appendChild(newItem_oc1);

                var newItem_oc2 = document.createElement('div');
                newItem_oc2.className = ('outgoing-chats-img');
                var userImg = "https://api.chatbotdev.roundsqr.net/" + css.user_logo;
                newItem_oc2.innerHTML = ('<img src= ' + userImg + '>');
                newItem_oc.appendChild(newItem_oc2);

                newItem_oc.scrollTop = newItem_oc.scrollHeight;

                responseContainer.appendChild(newItem_oc);
                responseContainer.scrollTop = responseContainer.scrollHeight;

                funChatbox(btnValue, ajaxResponse[0].question, response, ajaxResponse[0].sessionId);

            });
            span.appendChild(newbtn);
        }
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
        document.getElementsByClassName("msg-bottom")[0].style.backgroundColor = css.header_colour;
    } else {
        document.getElementById("bolForm").style.display = "none";
    }

    if (ajaxResponse[0].answer_type == 'FILE') {
        document.getElementById("fileForm").style.display = "block";
    } else {
        document.getElementById("fileForm").style.display = "none";
    }

    var finalSeconds = new Date().getTime() / 1000;
    console.log(finalSeconds);
    console.log(finalSeconds - seconds)
}


async function SaveFile(res) {
    let formData = new FormData();
    let file = res.files[0];
    let textmsg = file.name;
    let filePath;
    let response;
    formData.append("asset", file);

    try {
        let r = await fetch('https://api.chatbotdev.roundsqr.net/assets/file', { method: "POST", body: formData })
            .then(response => response.text())
            .then(data =>
                response = JSON.parse(data));
        console.log(response)

        if (response.status == 'success') {
            filePath = response.response;
            funFileMsg(textmsg, filePath);
        }
    } catch (e) {
        console.log('Powerbot we have problem...:', e);
    }

}

async function funFileMsg(textmsg, filePath) {
    var Url = "https://api.chatbotdev.roundsqr.net/bot-properties?source_url=";
    var params = window.location.href;
    var css;

    try {
        let r = await fetch(Url + params, { method: "GET" })
            .then(response => response.text())
            .then(data =>
                response = JSON.parse(data));
        console.log(response)

        if (response.status == 'success') {
            css = response.response;
        }
    } catch (e) {
        console.log('Abhee we have problem...:', e);
    }

    if (textmsg) {
        textmsg = textmsg;
        var responseContainer = document.querySelector('#responseContainer');
        // responseContainer.style.backgroundColor = css.body_color;

        var newItem_oc = document.createElement('div');
        newItem_oc.className = ('outgoing-chats');

        var newItem_oc1 = document.createElement('div');
        newItem_oc1.className = ('outgoing-chats-msg');
        var para_oc = document.createElement('p');
        //user chat bubble backgroundcolor
        para_oc.style.backgroundColor = css.user_bubble_colour;
        //user chat text color
        para_oc.style.color = css.chat_user_font_colour;

        var span_oc = document.createElement('span');
        //span_oc.innerHTML = document.forms["myForm"]["text_msg"].value;
        span_oc.innerHTML = textmsg;
        para_oc.appendChild(span_oc);
        newItem_oc1.appendChild(para_oc);
        newItem_oc.appendChild(newItem_oc1);

        var newItem_oc2 = document.createElement('div');
        newItem_oc2.className = ('outgoing-chats-img');
        var userImg = "https://api.chatbotdev.roundsqr.net/" + css.user_logo;
        newItem_oc2.innerHTML = ('<img src= ' + userImg + '>');
        newItem_oc.appendChild(newItem_oc2);

        newItem_oc.scrollTop = newItem_oc.scrollHeight;

        responseContainer.appendChild(newItem_oc);
        responseContainer.scrollTop = responseContainer.scrollHeight;

        funChatbox(filePath, '', response, sessionIdGlobal);
    } else {
        alert("Please enter your Text Message.")
    }
}




function doit_onkeypress(event) {
    if (event.keyCode == 13 || event.which == 13) {
        funTextMsg();
    }
}

async function funTextMsg() {
    var Url = "https://api.chatbotdev.roundsqr.net/bot-properties?source_url=";
    var params = window.location.href;
    var css;

    try {
        let r = await fetch(Url + params, { method: "GET" })
            .then(response => response.text())
            .then(data =>
                response = JSON.parse(data));
        console.log(response)

        if (response.status == 'success') {
            css = response.response;
            console.log(response)
        }
    } catch (e) {
        console.log('Powerbot we have problem...:', e);
    }

    if (document.getElementById("txtmsgid").value != '') {
        textmsg = document.getElementById("txtmsgid").value;
        console.log(css)

        console.log(document.getElementById("resquestion").innerHTML);
        var responseContainer = document.querySelector('#responseContainer');
        // responseContainer.style.backgroundColor = css.body_colour;

        var newItem_oc = document.createElement('div');
        newItem_oc.className = ('outgoing-chats');

        var newItem_oc1 = document.createElement('div');
        newItem_oc1.className = ('outgoing-chats-msg');
        var para_oc = document.createElement('p');
        //user chat bubble backgroundcolor
        para_oc.style.backgroundColor = css.user_bubble_colour;
        //user chat text color
        para_oc.style.color = css.chat_user_font_colour;

        var span_oc = document.createElement('span');
        //span_oc.innerHTML = document.forms["myForm"]["text_msg"].value;
        span_oc.innerHTML = document.getElementById("txtmsgid").value;;
        para_oc.appendChild(span_oc);
        newItem_oc1.appendChild(para_oc);
        newItem_oc.appendChild(newItem_oc1);

        var newItem_oc2 = document.createElement('div');
        newItem_oc2.className = ('outgoing-chats-img');
        var userImg = "https://api.chatbotdev.roundsqr.net/" + css.user_logo;
        newItem_oc2.innerHTML = ('<img src= ' + userImg + '>');
        newItem_oc.appendChild(newItem_oc2);

        newItem_oc.scrollTop = newItem_oc.scrollHeight;

        responseContainer.appendChild(newItem_oc);
        responseContainer.scrollTop = responseContainer.scrollHeight;

        funChatbox('', '', response, sessionIdGlobal);
    } else {
        alert("Please enter your Text Message.")
    }
}
