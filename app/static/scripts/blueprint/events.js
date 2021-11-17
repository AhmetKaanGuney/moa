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

// TODO remove this
// Add Buttons (in 'Group' menu and on the middle of two lists)
/* var addButtons = document.getElementsByName("add-selected")
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
} */

updateElements()

// After UPDATE ASSIGN THESE FUNCTIONS TO NEWLY CREATED ELEMENTS

/* ADD onclick function to all list items
    - check the item's type and what is currently displayed to the user
    - do the add remove operation according to it. */

var listItems = document.getElementsByClassName("list-group-item");

for (let i = 0; i < listItems.length; i++) {
    let li = listItems[i];
    li.onclick = function() {

        // console.log(li);

        // Get Selected Options attributes
        let selectBox = document.getElementById("user-group-select");
        let selectedGroup = selectBox.options[selectBox.selectedIndex];
        let selectedGroupName = selectedGroup.value;
        let selectedGroupType = selectedGroup.getAttribute("group-type");

        // Get clicked list items attributes
        let itemType = li.getAttribute("item-type");
        let itemName = li.textContent;

        /* Yields true if user clicks on source list item and
            it matches user list's group type */
        if (itemType === "source-row" && selectedGroupType === "row") {
            console.log("item: %s \nselected-group: %s", itemType, selectedGroupType);

            gm.addToRowGroups([itemName], selectedGroupName);
        }
        else if (itemType === "source-col" && selectedGroupType === "col") {
            console.log("item: %s \nselected-group: %s", itemType, selectedGroupType);

            gm.addToColGroups([itemName], selectedGroupName);
        }

        //  Get selected tab
        let selectedTab = document.getElementsByClassName("nav-link active").id;

        /* Yields true if user click on user list item and
        user list and selected tab are the same type */
        if (itemType === "user-row" && selectedTab === "row-tab") {
            console.log("item: %s \nselected-tab: %s", itemType, selectedTab);

            gm.removeItemFromRowGroup(itemName, selectedGroupName)
        }
        else if (itemType === "user-col" && selectedTab === "col-tab") {
            console.log("item: %s \nselected-tab: %s", itemType, selectedTab);

            gm.removeItemFromColGroup(itemName, selectedGroupName)
        }
    };
}
