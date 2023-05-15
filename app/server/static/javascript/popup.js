/* When the user clicks on the button, 
toggle between hiding and showing the Popup content */
function popupFunction() {
    document.getElementById("popup_menu").classList.toggle("show");
}

// Close the popup if the user clicks outside of it
window.onclick = function (event) {
    if (!event.target.matches('.popup')) {
        var popups = document.getElementsByClassName("popup-content");
        var i;
        for (i = 0; i < popups.length; i++) {
            var openPopup = popups[i];
            if (openPopup.classList.contains('show')) {
                openPopup.classList.remove('show');
            }
        }
    }
}

