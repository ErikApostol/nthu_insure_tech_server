const api_home = "/home";

async function home() {
    const response = await fetch(api_home);
    const data = await response.json();

    document.getElementById("your_video").textContent = data["your_video"];
    document.getElementById("all_video").textContent = data["all_video"];
    document.getElementById("number_of_user_registered").textContent = data["number_of_user_registered"];
    document.getElementById("visited").textContent = data["visited"];
}

home();