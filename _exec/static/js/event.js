const ticketDiv = document.querySelector("div#tickets");
const discordDiv = document.querySelector("div#discord")
const locationDiv = document.querySelector("div#location")

function showTickets() {
    ticketDiv.style.display = "block";
    discordDiv.style.display = "none";
    locationDiv.style.display = "none";

    document.querySelectorAll(".second-nav").forEach((item) => {
        item.classList.remove("active");
    });

    document.querySelector("#get-tickets").classList.add("active");
}

function showDiscord() {
    ticketDiv.style.display = "none";
    discordDiv.style.display = "block";
    locationDiv.style.display = "none";

    document.querySelectorAll(".second-nav").forEach((item) => {
        item.classList.remove("active");
    });

    document.querySelector("#join-discord-button").classList.add("active");
}

function showLocation() {
    ticketDiv.style.display = "none";
    discordDiv.style.display = "none";
    locationDiv.style.display = "block";

    document.querySelectorAll(".second-nav").forEach((item) => {
        item.classList.remove("active");
    });

    document.querySelector("#location-button").classList.add("active");
}