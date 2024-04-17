window.onload = function() {
    // Get the navbar element
    var navbar = document.querySelector("nav");

    // Get the computed height of the navbar
    var navbarHeight = window.getComputedStyle(navbar).getPropertyValue("height");

    // Display the computed height using an alert
    document.querySelector("input#search").style.height = navbarHeight;
};
