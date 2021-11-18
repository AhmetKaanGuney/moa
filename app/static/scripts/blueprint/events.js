import { gm } from "./globals.js";
import { modalWindow, modifyModal } from "./modalWindow.js";
import { updateLists, updateGroupSelect } from "./update.js";

/* Assign functions to button and call updateElements() on every button click */

// --------------------------- //
// --------- BUTTONS --------- //
// --------------------------- //

// CREATE GROUP BUTTON
document.getElementById("create-group").onclick = function() {
    console.log("create group()")

    modifyModal("Create Group", "Group Name", "create")
    modalWindow.show()
    document.getElementById("modal-input").focus();
}

// RENAME GROUP BUTTON
document.getElementById("rename-group").onclick = function() {
    console.log("rename group()")

    modifyModal("Rename Group", "New Group Name", "rename")
    modalWindow.show()
    document.getElementById("modal-input").focus();

}

// DELETE GROUP BUTTON
document.getElementById("delete-group").onclick = function() {
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

// ON GROUP SELECTION CHANGE
document.getElementById("user-group-select").onchange = function() {
    updateLists();
}