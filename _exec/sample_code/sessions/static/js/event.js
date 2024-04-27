const ticketDiv = document.querySelector("div#tickets");
const discordDiv = document.querySelector("div#discord");
const locationDiv = document.querySelector("div#location");

function show(element, activeButton) {
    ticketDiv.style.display = element === ticketDiv ? "block" : "none";
    discordDiv.style.display = element === discordDiv ? "block" : "none";
    locationDiv.style.display = element === locationDiv ? "block" : "none";

    document.querySelectorAll(".second-nav").forEach((item) => {
        item.classList.remove("active");
    });

    document.querySelector(activeButton).classList.add("active");
}

function showTickets() {
    show(ticketDiv, "#get-tickets");
}

function showDiscord() {
    show(discordDiv, "#join-discord-button");
}

function showLocation() {
    show(locationDiv, "#location-button");
}
