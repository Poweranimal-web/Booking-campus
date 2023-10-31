let current_rooms = [];
document.addEventListener("DOMContentLoaded", function () {
  const url = window.location.href;
  const floorButtons = document.querySelectorAll(".floor-button");
  const roomGrids = document.querySelectorAll(".room-grid");
  const continueButton = document.getElementById("continue-button");
  continueButton.addEventListener("click",click);
  floorButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const selectedFloor = this.dataset.floor;
      // Скрываем все сетки комнат
      roomGrids.forEach((grid) => (grid.style.display = "none"));

      // Показываем нужную сетку
      const activeGrid = document.querySelector(
        `[data-floor-grid="${selectedFloor}"]`
      );
      while (activeGrid.firstChild) {
        activeGrid.removeChild(activeGrid.firstChild);
      }
      get_rooms(selectedFloor).then(list_rooms => {
        current_rooms = list_rooms
        for (var i=0;i<current_rooms.length;i++){
          let data = current_rooms[i];
          if (Number(data["taken_beds"]) < Number(data["num_beds"])){
              const roomButton = document.createElement("button");
              roomButton.textContent = data["number"];
              roomButton.value = data["id"];
              activeGrid.appendChild(roomButton);
          }
        } 
      });;
      activeGrid.style.display = "grid";
      // Отменяем выбор комнаты, если был ранее
      const previouslySelected = activeGrid.querySelector("button.selected");
      if (previouslySelected) {
        previouslySelected.classList.remove("selected");
      }
      // continueButton.style.display = "none";
    });
  });

  roomGrids.forEach((grid) => {
    grid.addEventListener("click", function dm(event) {
      event.preventDefault();
      if (event.target.tagName === "BUTTON") {
        const selectedRoom = event.target;
        const id_room = event.target.value;
        const otherRooms = this.querySelectorAll("button");

        otherRooms.forEach((room) =>{
          room.classList.remove("selected");
        });

        selectedRoom.classList.add("selected");
        continueButton.style.display = "block";
        continueButton.value = id_room;
        
      }
    });
  });

  async function click(event) {
    event.preventDefault();
    const id_room = event.target.value;
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');  
    const response = await fetch(url,{
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        "status": "send_request",
        "id_room": id_room
    })
    
  });
  let data = await response.json();
  if (data["status"] == "not saved request"){
      let error = document.getElementById("error");
      error.textContent = data["error"];
      error.style.display = "block";

  }
  else if (data["status"] == "saved request"){
     window.location.href = "http://127.0.0.1:8000/admin-lite/applications/";

  }
}
  // Генерация комнат для каждого этажа
  // const numberOfRoomsPerFloor = 20;
  // roomGrids.forEach((grid, index) => {
  //   for (let i = 1; i <= numberOfRoomsPerFloor; i++) {
  //     const roomButton = document.createElement("button");
  //     roomButton.textContent = `${i + index * numberOfRoomsPerFloor}`; // чтобы комнаты на разных этажах имели разные номера
  //     grid.appendChild(roomButton);
  //   }
  // });
  async function get_rooms(floor){
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');
    const response = await fetch(url,{
      method: "POST",
      headers: headers,
      body: JSON.stringify({
        "status": "get_rooms",
        "floor_num": floor
    })

    });
    let data = await response.json();
    return data;
  }
});
