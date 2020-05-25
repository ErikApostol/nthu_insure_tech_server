const api_get_username = "/get_username";

async function get_username() {
    const response = await fetch(api_get_username);
    const data = await response.json();

    console.log(data);

    if(data["username"] == "") {
        document.getElementById("login_status").innerHTML = "請登入";
        document.getElementById("username").textContent = "zzz";
    } else {
        document.getElementById("username").textContent = data["username"];
    }
}

get_username();