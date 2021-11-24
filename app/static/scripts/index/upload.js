// On file upload store uploaded filename
let submitButton = document.getElementById("submit-button");

submitButton.onclick = function() {
    let filepath = document.getElementById("file-input").value;
    let filename = filepath.split("/");
    if (filename.length === 1) {
        filename = filepath.split("\\");
    }
    filename = filename[filename.length - 1];
    console.log(filename);
    sessionStorage["filename"] = filename;
}