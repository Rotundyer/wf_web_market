var item;

function load(host) {
  document.getElementById("wfm-id").value = "";
  document.getElementById("url-name").value = "";
  document.getElementById("trading-tax").value = "";
  document.getElementById("icon-url").value = "";
  document.getElementById("max-rank").value = "";
  document.getElementById("vosfor").value = "";
  document.getElementById("reputation").value = "";
  let value = document.getElementById("iclude-url").value;
  if (value.substr(0, 4) == "http") {
    value = value.replaceAll("https://warframe.market/items/", "");

    const request = new XMLHttpRequest();
    request.open(
      "POST",
      `http://${host}/get_item_from_wfm?url=${value}`,
      false
    );
    request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");

    request.onload = () => {
      console.log(`item: ${value}`);
      console.log(`status: ${request.status}`);

      const response_json = JSON.parse(request.response);

      document.getElementById("approve-info").style.visibility = "visible";
      document.getElementById("approve-hr").style.visibility = "visible";
      document.getElementById("approve-end-button").style.visibility =
        "visible";

      document.getElementById("wfm-id").value = response_json["wfm_id"];
      document.getElementById("url-name").value = response_json["url_name"];
      document.getElementById("trading-tax").value =
        response_json["trading_tax"];
      document.getElementById("icon-url").value = response_json["icon"];
      document.getElementById("max-rank").value = response_json["max_rank"];
      document.getElementById("vosfor").value = 0;
      document.getElementById("reputation").value = 0;
    };
    request.onerror = () => {
      show_toast("An error occurred while trying to load an item");
    };

    request.send();
  } else {
    show_toast("Incorrect link");
  }
}

function update_item(host) {
  const wfm_id = document.getElementById("wfm-id").value;
  const url_name = document.getElementById("url-name").value;
  const trading_tax = document.getElementById("trading-tax").value;
  const icon = document.getElementById("icon-url").value;
  const max_rank = document.getElementById("max-rank").value;
  const vosfor = document.getElementById("vosfor").value;
  const reputation = document.getElementById("reputation").value;
  const location = document.getElementById("location-select").value
  const in_pool = document.getElementById("input-checkbox").checked;

  if (wfm_id == "") {
    show_toast('Incorrect data in the field - "WFM ID"');
    return;
  }

  if (url_name == "") {
    show_toast('Incorrect data in the field - "URL Name"');
    return;
  }

  if (trading_tax == "") {
    show_toast('Incorrect data in the field - "Trading Tax"');
    return;
  }

  if (max_rank == "") {
    show_toast('Incorrect data in the field - "Max Rank"');
    return;
  }

  const request = new XMLHttpRequest();
  request.open(
    "POST",
    `http://${host}/create_item`,
    false
  );
  request.setRequestHeader("Content-Type", "application/json; charset=UTF-8");

  request.onload = () => {
    console.log(request.status);
    console.log(request.response);

      if (typeof(request.response) == 'string') {
        show_toast(request.response)
      }
  };

  request.onerror = () => {
    show_toast("An error occurred when adding an item to the database");
  };

  const body = JSON.stringify({
    wfm_id: wfm_id,
    url_name: url_name,
    trading_tax: parseInt(trading_tax),
    max_rank: parseInt(max_rank),
    icon: icon,
    vosfor: vosfor,
    reputation: reputation,
    in_pool: in_pool,
    location: location
  });

  request.send(body);
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

function isNotEmpty(elemId) {
  var elem = document.getElementById(elemId);
  var str = elem.value;
  var re = /.+/;
  if (!str.match(re)) {
    elem.style.border = "1px solid red";
    return false;
  } else {
    elem.style.border = "1px solid black";
    return true;
  }
}
