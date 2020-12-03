
(function() {
    var startingTime = new Date().getTime();
    // Load the script
    var script = document.createElement('script');
    script.src = 'https://api.chatbotdev.roundsqr.net/static/js/chatbotScripts-dev.js';
    script.type = 'text/javascript';
    document.getElementsByTagName('head')[0].appendChild(script);

    var link = document.createElement("LINK");
    link.setAttribute("rel", "stylesheet");
    link.setAttribute("type", "text/css");
    link.setAttribute("href", "https://api.chatbotdev.roundsqr.net/static/css/style.css");
    document.head.appendChild(link);

    var jScript = document.createElement("script");
    jScript.setAttribute("rel", "stylesheet");
    jScript.setAttribute("type", "text/javascript");
    jScript.setAttribute("href", "https://code.jquery.com/jquery-3.5.1.js");
    document.head.appendChild(jScript);


    // var link1 = document.createElement("LINK");
    // link1.setAttribute("rel", "stylesheet");
    // link1.setAttribute("type", "text/css");
    // link1.setAttribute("href", "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css");
    // document.head.appendChild(link1);

    var link2 = document.createElement("LINK");
    link2.setAttribute("rel", "stylesheet");
    link2.setAttribute("type", "text/css");
    link2.setAttribute("href", "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");
    document.head.appendChild(link2);

    // Poll for jQuery to come into existance
    var checkReady = function(callback) {
        if (window.jQuery) {
            callback(jQuery);
        }
        else {
            window.setTimeout(function() { checkReady(callback); }, 20);
        }
    };

    // Start polling...
    checkReady(function($) {
        $(document).ready(function () {
            $('#rsq_box').on('click', function () {
                $('#rsq_chat-box').fadeIn(400);
                $(this).fadeOut(100);
            });
            $('#rsq_chat-box #rsq_minimize').on('click', function () {
                $('#rsq_chat-box').slideUp(600);
                $('#rsq_box').fadeIn(400);
            });
        });
    })
})();
