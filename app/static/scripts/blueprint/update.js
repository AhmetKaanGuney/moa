import { gm } from "./globals.js";

function updateSourceLists() {
    /*
     * Updates these source row and column lists according to
     * gm.sourceRows, gm.sourceCols
     * gm is GroupManager object constructed with blueprint
     * that comes from server
    */

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

    let sourceRowsList = document.getElementById("source-rows-list")
    let sourceColsList = document.getElementById("source-cols-list")

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
    let groupType = selected.getAttribute("group-type");
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

    // get all the user group names
    let rowGroupNames = Object.keys(gm.userRowGroups);
    let colGroupNames = Object.keys(gm.userColGroups);

    // get select
    let groupSelect = document.getElementById("user-group-select");

    // clone options that are indicators
    let rowClone = document.getElementById("group-select-option-row").cloneNode(true);
    let colClone = document.getElementById("group-select-option-col").cloneNode(true);

    // remove childeren of select
    while (groupSelect.firstChild) {
        groupSelect.removeChild(groupSelect.firstChild);
    }

    // add ROWS option first
    groupSelect.appendChild(rowClone);

    // generate new options and append
    for (let i = 0; i < rowGroupNames.length; i++) {
        let itemName = rowGroupNames[i];

        let opt = document.createElement("option");
        opt.value = opt.textContent = itemName;
        opt.setAttribute("group-type", "row");

        groupSelect.appendChild(opt);
    }

    // append COLUMNS option
    groupSelect.appendChild(colClone);

    // generate new options and append
    for (let i = 0; i < colGroupNames.length; i++) {
        let itemName = colGroupNames[i];

        let opt = document.createElement("option");
        opt.value = opt.textContent = itemName;
        opt.setAttribute("group-type", "col");

        groupSelect.appendChild(opt);
    }
}

export function updateElements() {
    updateSourceLists()
    updateUserList()

    updateGroupSelect()
};