import { gm } from "./globals.js";
import { updateElements } from "./update.js";

// Modal Window Object
var modalWindow = new bootstrap.Modal(document.getElementById("modal"));


// Change modals title, placeholderText and action type (for the button)
const modifyModal = function(title, placeholderText, buttonAction) {
    // Change Title
    document.getElementById("modal-title").textContent = title;

    // Clear input field and put place holder text
    document.getElementById("modal-input").value = "";
    document.getElementById("modal-input").placeholder = placeholderText;

    // Assign action attribute to button
    document.getElementById("modal-ok-button").setAttribute("action", buttonAction);
}


// Assign onclick to modalWindow's 'Okay' button
document.getElementById("modal-ok-button").onclick = function() {
    let action = document.getElementById("modal-ok-button").getAttribute("action");
    console.log("Action type %s", action);

    // Get selected option element
    let select = document.getElementById("user-group-select");
    let selected = select.options[select.selectedIndex];

    if (action === "create") {
        let inputValue = document.getElementById("modal-input").value;


        let groupType = selected.getAttribute("group-type");

        if (groupType === "row") {
            gm.createRowGroup(inputValue);
        }

        else if (groupType === "col") {
            gm.createColGroup(inputValue);
        }
    }

    if (action === "rename") {
        let selectedGroupName = selected.value;

        // inputValue is new group name
        if (groupType === "row") {
            gm.renameRowGroup(inputValue, selectedGroupName);
        }
        else if (groupType === "col") {
            gm.renameColGroup(inputValue, selectedGroupName);
        }
    }
    modalWindow.hide()
    updateElements()

    console.log(gm)
}


export { modalWindow, modifyModal };