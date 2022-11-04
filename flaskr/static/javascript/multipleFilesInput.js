var idnum = 0;

function addFileInput() {
    var template = document.getElementById("template");
    var clone = template.cloneNode(true);
    var parent = document.getElementById("container");
    var button = clone.querySelector("button");
    var input = clone.querySelector("input");

    button.id = idnum;
    input.id = idnum;
    clone.removeAttribute("id");
    clone.id = idnum;
    clone.removeAttribute("style");
    parent.appendChild(clone);

    var hr = document.createElement("hr")
    parent.appendChild(hr);
    idnum += 1;
}

function removeFileInput(id) {
    var child = document.getElementById(id);
    var parent = child.parentElement;
    var hr = parent.querySelector("hr");
    parent.removeChild(hr);
    child.remove();
}
