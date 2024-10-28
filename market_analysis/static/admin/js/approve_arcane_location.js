function on_click(host) {
  const value = document.getElementById("location-input").value;
  document.getElementById("location-input").value = "";

  if (value != "") {
    const request = new XMLHttpRequest();
    request.open("POST", `http://${host}/add_arcane_location`, false);
    request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");

    const body = JSON.stringify({
      name: `${value}`,
    });

    request.onload = () => {
      console.log(`Status code: ${request.status}`);
      console.log(request.response);

      const response_json = JSON.parse(request.response);

      if (response_json["id"] == undefined) {
        show_toast(response_json);
      } else {
        const table_ref = document
          .getElementById("location-table")
          .getElementsByTagName("tbody")[0];

        const row = table_ref.insertRow(0);

        const id_cell = document.createElement("th", { scope: "row" });
        id_cell.innerText = JSON.parse(request.response)["id"];

        const name_cell = document.createElement("td");
        name_cell.innerText = JSON.parse(request.response)["name"];

        row.appendChild(id_cell);
        row.appendChild(name_cell);
      }
    };

    request.send(body);
  } else {
    show_toast("The container is empty");
  }
}

function show_toast(message) {
  const toast = document.querySelector(".toast");
  const progress = document.querySelector(".toast-progress");
  const text = document.querySelector(".toast-text");

  toast.classList.add("active");
  progress.classList.add("active");
  text.textContent = message;

  setTimeout(() => {
    toast.classList.remove("active");
  }, 5000);

  setTimeout(() => {
    progress.classList.remove("active");
  }, 5300);
}
