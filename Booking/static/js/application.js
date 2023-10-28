const delete_btn = document.getElementsByClassName("abandon-btn");
const url = "http://127.0.0.1:8000/admin-lite/applications/";
for (var i = 0; i < delete_btn.length; i++) {
    delete_btn[i].addEventListener('click', delete_application);
}
async function delete_application(event){
    event.preventDefault();
    let id_app = event.target.value;
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    const response = await fetch(url,{
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            "status":"delete application",
            "id": id_app
        })
});
let res =  await response.json();
if (res["status"] == "deleted"){
    window.location.reload();
}

}