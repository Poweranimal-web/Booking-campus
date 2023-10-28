const url = "http://127.0.0.1:8000/admin-lite/profile/";
const update_form = document.getElementById("form");
update_form.addEventListener("submit",update_data);
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
async function set_data(){
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    const response = await fetch(url,{
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            "status":"get_data_user"
        })
});
let data_user =  await response.json();
console.log(data_user);
document.getElementById("name").value = data_user["first_name"];
document.getElementById("surname").value = data_user["last_name"];
document.getElementById("email").value = data_user["email"];
document.getElementById("password").value = data_user["password"];
document.getElementById("phone").value = data_user["contact_number"];
document.getElementById("profile-photo").src = "/media/"+data_user["profile_photo"];

}
set_data();
function check_match_passwords(password, repeat_password){
    if (password !=repeat_password){
        return "Паролі не совпадаються будь ласка введіть вірно.";
    }
    return true;
}
async function update_data(event){
    event.preventDefault();
    let match_passwords = check_match_passwords(document.getElementById("password").value,document.getElementById("repeatPassword").value);
    if (match_passwords == true){
        let headers = new Headers();
        headers.append('Content-Type', 'multipart/form-data');
        headers.append('Accept', 'multipart/form-data');
        let formData = new FormData();
        formData.append("text_data",JSON.stringify({
            "status":"update_data",
            "first_name": document.getElementById("name").value,
            "last_name": document.getElementById("surname").value,
            "email": document.getElementById("email").value,
            "contact-phone": document.getElementById("phone").value,
            "password": document.getElementById("password").value,
        }));
        formData.append("photo",document.getElementById("changeAvatar").files[0]);
        const response = await fetch(url,{
            method: "POST",
            // headers: headers,
            body: formData,
        });
        let data = await response.json();
        if (data["status"] =="updated"){
            window.location.reload();
        }
    }
    else{
        let error = document.getElementById("error");
        error.textContent = match_passwords;
        error.style.display = "block";
    }


}