
function viewContent(id) {
    var parent = document.getElementById(id);
    var viewContent = parent.querySelector(".view_content");
    viewContent.style.display = "flex";
    var viewButton = parent.querySelector("li.view_button");
    viewButton.innerHTML = "Hide";
    viewButton.setAttribute("onclick","hideContent(this.id)");
    
}

function hideContent(id) {
    var parent = document.getElementById(id);
    var viewContent = parent.querySelector(".view_content");
    viewContent.style.display = "none";
    var viewButton = parent.querySelector("li.view_button");
    viewButton.innerHTML = "View";
    viewButton.setAttribute("onclick","viewContent(this.id)");

}


