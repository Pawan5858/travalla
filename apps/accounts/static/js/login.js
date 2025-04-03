var org_details = {
    "act_id": 1,
    "logo": "/static/images/logos/swc_logo.png",
    "org_id": 1,
    "status": "AC",
    "title": "Chikitsayam",
    "website": "https://chikitsayam.com/"
};

var web_fcm_token = null;

$(function () {
    formSubmit = true;
    var firebaseConfig = {
        apiKey: "AIzaSyAdwbaGGOVejWaU7FIRuvZoHICZdBiRQBI",
        authDomain: "agilepolicepush.firebaseapp.com",
        databaseURL: "https://agilepolicepush-default-rtdb.firebaseio.com",
        projectId: "agilepolicepush",
        storageBucket: "agilepolicepush.appspot.com",
        messagingSenderId: "87968458837",
        appId: "1:87968458837:web:a803389b8ed32c1b5f0cdc",
        measurementId: "G-8TSK1E9F9E"
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    firebase.analytics();
    const messaging = firebase.messaging();
    console.log(messaging.getToken());
    messaging.getToken({ vapidKey: 'BJ6iruoLynVVtdxsbmAbAecdMqrmjYgyIjmxhbpdbf8AuTMg8Bb0HhVGJSKdg4O7SbREnCoExpV73QJ-odVh3jc' })
        .then((currentToken) => {
            if (currentToken) {
                web_fcm_token = currentToken;
            } else {
                console.log('No registration token available. Request permission to generate one.');
            }
        })
        .catch((err) => {
            console.log('An error occurred while retrieving token. ', err);
        });
    messaging.requestPermission()
        .then(function () {
            console.log("Notification permission granted.");
            return messaging.getToken();
        })
        .catch(function (err) {
            console.log("Unable to get permission to notify.", err);
        });
    messaging.onMessage((payload) => {
        console.log('Message received. ', payload);
    });
});

$('#usrName, #usrPwd').keypress(function (event) {
    var keycode = (event.keyCode ? event.keyCode : event.which);
    if (keycode == '13') {
        loginBtnAction(); // Trigger login directly
    }
});

function loginBtnAction() {
    var formEle = '#loginForm';
    $('#loginForm').addClass('was-validated');

    if (validateForm(formEle)) {
        // Check domain condition
        if (document.domain === '192.168.108.112' || document.domain === '142.93.220.180') {
            loginAPICall(null); // No reCAPTCHA for these domains
        } else {
            grecaptcha.ready(function () {
                grecaptcha.execute(reCAPTCHA_SITE_KEY, { action: 'login' }).then(function (token) {
                    loginAPICall(token); // Pass reCAPTCHA token
                }).catch(function (error) {
                    console.error("reCAPTCHA execution failed:", error);
                    show_StatusModal("reCAPTCHA verification failed", "error");
                });
            });
        }
    }
}

function loginAPICall(token) {

    
    var loginForm = document.getElementById("loginForm");
    var formData = new FormData(loginForm);
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    // Add encrypted password and FCM token
    formData.set('password', rsa_encrypt.encrypt(formData.get('password')));
    formData.append('web_fcm_token', web_fcm_token);

    // Add reCAPTCHA token if available
    if (token) {
        formData.append('recaptcha_token', token);
    }

    $.ajax({
        url: baseUrl + 'login/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        headers: {
            "X-CSRFToken": csrftoken
        },
        success: function (result) {
            console.log("result.status", result.status)
            if (apiResStatus(result.status)) {
                
                addMainUserSession(result.user);
                window.location.href = "/clientAdmin/dashboard/";
            } else {
                console.log("error block")
                console.log("error block")
                console.log("error block")
                console.log("error block")
                console.log("error block")
                show_StatusModal(result.message, result.status);
            }
        },
        error: function (xhr, status, error) {
            console.error("Login API error:", error);
            errorCallBack(xhr, status, error);
        }
    });
}

function resetBtnAction() {
    var formEle = '#resetForm';
    $('#resetForm').addClass('was-validated');

    if (validateForm(formEle)) {
        var resetForm = document.getElementById("resetForm");
        var formData = new FormData(resetForm);
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        $.ajax({
            url: baseUrl + 'admin/resetPasswordLink',
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            success: function (result) {
                show_StatusModal(result.message, result.status);
            },
            error: errorCallBack
        });
    }
}

function openForgotPwdSection() {
    $('#option3').trigger('click');
}

function openLoginSection() {
    $('#option1').trigger('click');
}

$(document).on('click', '.toggle-password', function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $("#usrPwd");
    input.attr('type') === 'password' ? input.attr('type', 'text') : input.attr('type', 'password');
});