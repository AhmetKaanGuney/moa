import { gm } from "./globals.js";
import { modalWindow, modifyModal } from "./modalWindow.js";
import { updateLists, updateGroupSelect } from "./update.js";

/* Assign functions to button and call updateElements() on every button click */

// --------------------------- //
// ------- FUNCTIONS --------- //
// --------------------------- //
function createGroup() {
    console.log("create group()");

    modifyModal("Create Group", "Group Name", "create");
    modalWindow.show();
    document.getElementById("modal-input").focus();
}

function renameGroup() {
    console.log("rename group()");

    modifyModal("Rename Group", "New Group Name", "rename");
    modalWindow.show();
    document.getElementById("modal-input").focus();
}

function deleteGroup() {
    console.log("delete group");
    // Get selected group
    let select = document.getElementById("user-group-select");
    let selectedGroup = select.options[select.selectedIndex];

    let selectedGroupName = selectedGroup.value;
    let selectedGroupType = selectedGroup.getAttribute("group-type");

    console.log("Deleting : %s", selectedGroupName);

    if (selectedGroupType === "row") {
        gm.deleteRowGroup(selectedGroupName);
    } else if (selectedGroupType === "col") {
        gm.deleteColGroup(selectedGroupName);
    }
    updateGroupSelect(null, null, true);
    updateLists();
}
// --------------------------- //
// --------- BUTTONS --------- //
// --------------------------- //
// CREATE GROUP
document.getElementById("create-group").onclick = createGroup;

// RENAME GROUP BUTTON
document.getElementById("rename-group").onclick = function() {renameGroup();};


// DELETE GROUP BUTTON
document.getElementById("delete-group").onclick = function() {deleteGroup();};

// ON GROUP SELECTION CHANGE
document.getElementById("user-group-select").onchange = function() {

    // Get selected group option
    let select = document.getElementById("user-group-select");
    let selectedGroup = select.options[select.selectedIndex];

    if (selectedGroup.hasAttribute("group-type") === false) return;

    let selectedGroupType = selectedGroup.getAttribute("group-type");

    let tabButton = {};
    if (selectedGroupType === "row") {
        // tab = ROWS
        tabButton = document.getElementById("row-tab");
    } else if (selectedGroupType === "col"){
        // tab = COLS
        tabButton = document.getElementById("col-tab");
    }
    // toggle tab
    tabButton.click();
    updateLists();
}

export { createGroup, deleteGroup, renameGroup }