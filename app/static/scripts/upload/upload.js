// On file upload store uploaded filename
let submitButton = document.getElementById("submit-button");

submitButton.onclick = function() {
    let filename = document.getElementById("file-input").value;
    sessionStorage["filename"] = filename;
}