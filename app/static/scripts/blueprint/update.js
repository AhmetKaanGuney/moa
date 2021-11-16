import { gm } from "./globals.js"

function updateSourceLists() {
    /**
     * Updates these Elements according to Group Manager object ('gm'):
     *      - source row and col lists
     */

    // --------------- //
    // ---- TOOLS ---- //
    // --------------- //

    // Updates List Element
    const updateListElement = function(items, parent) {
        // Reset parent
        while (parent.firstChild) {
            parent.removeChild(parent.firstChild);
        }

        // Append to parent
        for (let i = 0; i < items.length; i++) {
            let itemName = items[i];
            let li = document.createElement("li");
            li.className = "list-group-item";
            li.textContent = itemName;
            parent.appendChild(li);
        }
    };

    // Get which option is selected ('rows' or 'cols')
    let selectElement = document.getElementById("source-list-select");
    let selection = selectElement[selectElement.selectedIndex].value;

    // Render selected option
    if (selection === "rows") {
        updateListElement(gm.sourceRows, sourceRowsList);

        // Hide col list and display row list
        sourceRowsList.hidden = false;
        sourceColsList.hidden = true;
    }
    if (selection === "cols") {
        updateListElement(gm.sourceCols, sourceColsList);

        // Hide row list and display col list
        sourceRowsList.hidden = true;
        sourceColsList.hidden = false;
    }
}

function updateUserList() {
    // Render User List according to user's group selection

    // get which group is selected
    let selectElement = document.getElementById("user-group-select");
    let selected = selectElement[selectElement.selectedIndex];
    let groupName = selected.value;

    let groupItems = Array();
    let groupType = selected.getAttribute("group-type")
    // get selected groups type
    if (groupType === "row") {
        // if type is row-group
        groupItems = gm.getRowGroup(groupName);
    }
    else if (groupType === "col") {
        // if type is col-group
        groupItems = gm.getColGroup(groupName);
    }

    // remove all children of user list
    let userList = document.getElementById("user-list");
    while (userList.firstChild) {
        userList.removeChild(userList.firstChild);
    }

    // generate list item from group items
    for (let i = 0; i < groupItems.length; i++) {
        let itemName = groupItems[i];

        let li = document.createElement("li");
        li.className = "list-group-item";
        li.textContent = itemName;

        // append new list items to user list
        userList.appendChild(li);
    }
}


function updateGroupSelect() {

    // get all the userRowGroup names
    let rowGroupNames = Object.keys(gm.userRowGroups)

    // remove childeren of select except options that
    //                        has attribute permanent

    // TODO ITERATE PROPERLY THROUGH OPTION
    let groupSelect = document.getElementById("user-group-select")
    for (let i = 0; i < groupSelect.length; i++) {
        console.log(groupSelect[i])
    }

    // generate new options
    // skip ROW option
    // append AFTER option ROW

    // get all the userColGroup names

    // generate new options
    // append AFTER option COL meaning last

    // option.setAttribute("group-type", groupType);
    return;
}

