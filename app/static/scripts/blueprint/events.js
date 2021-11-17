import { gm } from "./globals.js";
import { modalWindow, modifyModal } from "./modalWindow.js";
import { updateElements } from "./update.js";

/* Assign functions on events */

// SELECTS
var sourceSelect = document.getElementById("source-groups-select")
var userGroupSelect = document.getElementById("user-groups-select")

// --------------------------- //
// --------- BUTTONS --------- //
// --------------------------- //

// Create Group -Button
document.getElementById("create-group").onclick = function() {
    console.log("create group()")

    modifyModal("Create Group", "Group Name", "create")

    // Unhide select box in the modalWindow
    document.getElementById("modal-group-type-select").hidden = false

    modalWindow.show()
}

// Delete Group -Button
document.getElementById("delete-group").onclick = function() {
    console.log("delete group ()\n--- TODO ---")
}

// Rename Group -Button
document.getElementById("rename-group").onclick = function() {
    console.log("rename group()")

    modifyModal("Rename Group", "New Group Name", "rename")
    // Hide select box
    document.getElementById("modal-group-type-select").hidden = true
    modalWindow.show()
}

// Add Buttons (in 'Group' menu and on the middle of two lists)
var addButtons = document.getElementsByName("add-selected")
for (let i = 0; i < addButtons.length; i++) {
    addButtons[i].onclick = function() {
        console.log("add selected()")
    }
}

// Remove Buttons (at the same places with add buttons)
var removeButtons = document.getElementsByName("remove-selected")
for (let i = 0; i < removeButtons.length; i++) {
    removeButtons[i].onclick = function() {
        console.log("remove selected()")
    }
}

/* ADD onclick function to all list items
    - check the itemType then
    - do the add remove operation according to it. */

updateElements()