var modal = document.querySelector(".modal-container");
var close_btn = document.getElementById("close-button");
var btn = document.getElementById("click");
var form_reg = document.getElementById("form_reg");
btn.addEventListener("click", show_register_modal);
close_btn.addEventListener("click", close_modal);
form_reg.addEventListener("submit", create_user);
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
function show_register_modal(event){
    event.preventDefault();
    modal.style.display = "flex";
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
async function create_user(event){
    event.preventDefault();
    let password_valid =  await check_match_passwords(document.getElementById("password").value,document.getElementById("repeat_password").value);
    console.log(password_valid);
    if (password_valid == true){
            const select = document.getElementById('faculty');
            const response = await fetch("http://localhost:8000/",{
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrftoken
            },
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
            window.location.reload();
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