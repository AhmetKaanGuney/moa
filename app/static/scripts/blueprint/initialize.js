import { gm } from "./globals.js";
import { updateLists } from "./update.js";
import { createGroup, deleteGroup, renameGroup } from "./events.js";

var initialized = false;

if (initialized == false) {

    updateLists()

    // Put uploaded filename to left top corner
    // let filepath = sessionStorage["filename"].split("\\");
    // let filename = filepath[filepath.length - 1];
    // document.getElementById("filename-display").textContent = filename;
    let length = gm.sourceRows.length;
    for (let i = 0; i < 100; i++) {
        let li = document.createElement("li");
        li.className = "list-group-item";
        li.textContent = i;
        // li.style = "color: rgba(0, 0, 0, 0)";
        document.getElementById("user-list").appendChild(li);
    }


    // Add event listener when user hits enter on the modalWindow
    document.getElementById("modal-input").addEventListener("keyup", function(event) {
        // Enter = 13
        if (event.key === "Enter") {
            document.getElementById("modal-ok-button").click();
        }
    });

    // ---------------------------- //
    // ----- ASSIGN SHORTCUTS ----- //
    // ---------------------------- //
    document.addEventListener("keyup", function(event) {
        // console.log(event.key, "CTRL: " + event.ctrlKey, " ALT: " + event.altKey);

        // TODO export onclick functions
        // CTRL + ALT + G --> [Create Group]
        if ((event.ctrlKey && event.altKey) && (event.key === "g" || event.key === "G")) {
            event.preventDefault();
            createGroup();
        }
        // CTRL + ALT + D --> [Delete Group]
        if ((event.ctrlKey && event.altKey) && (event.key === "d" || event.key === "D")) {
            event.preventDefault();
            deleteGroup();
        }
        // CTRL + ALT + R --> [Rename Group]
        if ((event.ctrlKey && event.altKey) && (event.key === "r" || event.key === "R")) {
            event.preventDefault();
            renameGroup();
        }
    })

    initialized = true;
}