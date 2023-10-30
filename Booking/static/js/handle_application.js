const url = "http://127.0.0.1:8000/admin-lite/applications/";
let btn_accept = document.getElementsByClassName("accept-btn");
let btn_decline = document.getElementsByClassName("decline-btn");
for(var i=0;i<btn_accept.length;i++){
    btn_accept[i].addEventListener("click",accept_application);
}
for(var i=0;i<btn_decline.length;i++){
    btn_decline[i].addEventListener("click",decline_application);
}
async function decline_application(event){
    const id = event.target.value;
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    const response = await fetch(url,{
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            "status":"decline application",
            "id": id
        })

    });
    const res = await response.json();
    if (res["status"] == "declined"){
        window.location.reload();
    }
}
async function accept_application(event){
    const id = event.target.value;
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    const response = await fetch(url,{
        method: "POST",
        headers: headers,
        body: JSON.stringify({
            "status":"accept application",
            "id": id
        })

    });
    const res = await response.json();
    if (res["status"] == "accepted"){
        window.location.reload();
    }
}