var modal = document.querySelector("#modal-window");
var modal_login = document.getElementById("modal-login");
var close_btn = document.getElementById("close-button");
var close_btn_login = document.getElementById("close-button-login");
var open_login_modal_button = document.getElementById("login-button");
var btn = document.getElementById("click");
var form_reg = document.getElementById("form_reg");
var form_login = document.getElementById("form_login")
btn.addEventListener("click", show_register_modal);
open_login_modal_button.addEventListener("click", show_login_modal);
close_btn.addEventListener("click", close_modal);
form_reg.addEventListener("submit", create_user);
form_login.addEventListener("submit", check_user);
close_btn_login.addEventListener("click",close_modal_login);
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function show_register_modal(event){
    event.preventDefault();
    modal.style.display = "flex";
}
function show_login_modal(event){
    event.preventDefault();
    let error = document.getElementById("error");
    modal.style.display = "none";
    error.style.display = "none";
    document.getElementById("first").value = "";
    document.getElementById("last").value = "";
    document.getElementById("email").value = "";
    document.getElementById("password").value ="";
    document.getElementById("repeat_password").value ="";
    modal_login.style.display = "flex";

}
function close_modal_login(event){
    event.preventDefault();
    let error = document.getElementById("error-login");
    error.style.display = "none";
    modal_login.style.display = "none";
    document.getElementById("email-login").value = "";
    document.getElementById("password-login").value ="";
}

function close_modal(event){
    event.preventDefault();
    let error = document.getElementById("error");
    modal.style.display = "none";
    error.style.display = "none";
    document.getElementById("first").value = "";
    document.getElementById("last").value = "";
    document.getElementById("email").value = "";
    document.getElementById("password").value ="";
    document.getElementById("repeat_password").value ="";

}
function check_match_passwords(password, repeat_password){
    if (password !=repeat_password){
        return "Паролі не совпадаються будь ласка введіть вірно.";
    }
    return true;
}
async function check_user(event){
    event.preventDefault();
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    headers.append("X-Requested-With", "XMLHttpRequest");
    // headers.append('X-CSRFToken', getCookie("csrftoken"));
    const response = await fetch("http://127.0.0.1:8000/",{
            method: "POST",
            headers: headers,
            credentials: "same-origin",
            body: JSON.stringify({
                "status": "check_user",
                "email": document.getElementById("email-login").value,
                "password": document.getElementById("password-login").value,
            })
        });
    let data = await response.json();
    if (data["status"] =="exist_account"){
        document.location.href = 'http://127.0.0.1:8000/admin-lite/profile/';
    }
    else if (data["status"] == "not_exist_account"){
            let error = document.getElementById("error-login");
            error.textContent = data["error"];
            error.style.display = "block";
    }

}
async function create_user(event){
    event.preventDefault();
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    headers.append("X-Requested-With", "XMLHttpRequest");
    // headers.append('X-CSRFToken', getCookie("csrftoken"));
    let password_valid =  await check_match_passwords(document.getElementById("password").value,document.getElementById("repeat_password").value);
    if (password_valid == true){
            const select = document.getElementById('faculty');
            const response = await fetch("http://127.0.0.1:8000/",{
            method: "POST",
            headers:  headers,
            credentials: "same-origin",
            body: JSON.stringify({
                "status": "create_user",
                "faculty": select.options[select.selectedIndex].text,
                "first_name": document.getElementById("first").value,
                "last_name": document.getElementById("last").value,
                "email": document.getElementById("email").value,
                "password": document.getElementById("password").value,
            })
        });
        let data = await response.json();
        if (data["status"] =="created account"){
            document.location.href = 'http://127.0.0.1:8000/admin-lite/profile/';
        } 
        else if(data["status"] =="exist_account"){
            let error = document.getElementById("error");
            error.textContent = data["error"];
            error.style.display = "block";
        }
    }
    else{
        let error = document.getElementById("error");
        error.textContent = password_valid;
        error.style.display = "block";
        
    }
}