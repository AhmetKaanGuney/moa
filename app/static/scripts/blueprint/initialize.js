import { updateLists } from "./update.js";

var initialized = false;

if (initialized == false) {
    updateLists()

    // Put uploaded filename to left top corner
    let filepath = sessionStorage["filename"].split("\\");
    let filename = filepath[filepath.length - 1];
    document.getElementById("filename-display").textContent = filename;


    // Add event listener when user hits enter on the modalWindow
    document.getElementById("modal-input").addEventListener("keyup", function(event) {
        // Enter = 13
        if (event.key === "Enter") {
            document.getElementById("modal-ok-button").click();
        }
    });

    // ASSIGN SHORTCUTS
    document.addEventListener("keyup", function(event) {
        // console.log(event.key, "CTRL: " + event.ctrlKey, " ALT: " + event.altKey);

        // TODO export onclick functions
        // CTRL + ALT + G --> [Create Group]
        if ((event.ctrlKey && event.altKey) && (event.key === "g" || event.key === "G")) {
            event.preventDefault();
            console.log("CTRL + ALT + G");
        }
        // CTRL + ALT + D --> [Delete Group]
        if ((event.ctrlKey && event.altKey) && (event.key === "d" || event.key === "D")) {
            event.preventDefault();
            console.log("CTRL + ALT + D --> [Delete Group]");
        }
        // CTRL + ALT + R --> [Rename Group]
        if ((event.ctrlKey && event.altKey) && (event.key === "r" || event.key === "R")) {
            event.preventDefault();
            console.log("CTRL + ALT + R --> [Rename Group]");
        }
    })

    initialized = true;
}