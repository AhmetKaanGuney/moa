export function showErrorMessage(msg) {
    let box = document.getElementById("error-message-box");
    let p = document.getElementById("error-message");
    p.textContent = msg;
    box.hidden = false;
    setTimeout(function () {
        p.textContent = "";
        box.hidden = true;
    }, 5000)
}