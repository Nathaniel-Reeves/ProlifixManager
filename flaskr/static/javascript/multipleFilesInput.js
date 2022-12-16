var idnum = 0;

function addFileInput() {
    var template = document.getElementById("template");
    var clone = template.cloneNode(true);
    var parent = document.getElementById("container");
    var button = clone.querySelector("button");
    var input = clone.querySelector("input");

    button.id = idnum;
    input.id = idnum;
    input.name = idnum;
    clone.removeAttribute("id");
    clone.id = idnum;
    clone.removeAttribute("style");
    parent.appendChild(clone);

    idnum += 1;
}

function removeFileInput(id) {
    var child = document.getElementById(id);
    child.remove();
}
