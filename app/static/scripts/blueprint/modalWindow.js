import { gm } from "./globals.js";
import { updateGroupSelect, updateLists } from "./update.js";

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

    if (buttonAction === "create") {
        document.getElementById("modal-group-type-select").hidden = false;
    } else if (buttonAction === "rename") {
        document.getElementById("modal-group-type-select").hidden = true;
    }
}

// Assign onclick to modalWindow's 'Okay' button

document.getElementById("modal-ok-button").onclick = function() {
    let action = document.getElementById("modal-ok-button").getAttribute("action");
    console.log("Action type %s", action);

    let inputValue = document.getElementById("modal-input").value;
    if (inputValue === "") return;

    // CREATE ACTION
    if (action === "create") {
        let groupName = inputValue;

        // Get group type from modal selectbox
        let modalSelect = document.getElementById("modal-group-type-select");
        let modalSelectedGroupType = modalSelect.options[modalSelect.selectedIndex].value;

        if (modalSelectedGroupType === "row") {
            gm.createRowGroup(groupName);
            updateGroupSelect(groupName, "row");

        } else if (modalSelectedGroupType === "col") {
            gm.createColGroup(groupName);
            updateGroupSelect(groupName, "col");

        } else if (modalSelectedGroupType === "both") {
            gm.createRowGroup(groupName);
            gm.createColGroup(groupName);
            updateGroupSelect(groupName, "row");
        }
    }
    // RENAME ACTION
    else if (action === "rename") {
        let newName = inputValue;

        // Get user group selection from Group Select Dropdbox
        let sel = document.getElementById("user-group-select");
        let selectedGroup = sel.options[sel.selectedIndex];
        let selectedGroupType = selectedGroup.getAttribute("group-type");
        let selectedGroupName = sel.options[sel.selectedIndex].value;

        // inputValue is new group name
        if (selectedGroupType === "row") {
            gm.renameRowGroup(newName, selectedGroupName);
            updateGroupSelect(newName, selectedGroupType);

        } else if (selectedGroupType === "col") {
            gm.renameColGroup(newName, selectedGroupName);
            updateGroupSelect(newName, selectedGroupType);
        }
    }
    modalWindow.hide();
    console.log(gm);

    // Trigger onchange so that the right tab will automatically gets selected
    document.getElementById("user-group-select").onchange();
    updateLists();
}


export { modalWindow, modifyModal };