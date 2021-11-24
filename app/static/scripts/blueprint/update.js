import { gm } from "./globals.js";

/* ADD onclick function to all list items
    - check the item's type and what is currently displayed to the user
    - do the add remove operation according to it. */
function addOnclickFunctionToListItem(li) {

    li.onclick = function() {
        // Get Selected Options attributes
        let selectBox = document.getElementById("user-group-select");
        let selectedGroup = selectBox.options[selectBox.selectedIndex];
        let selectedGroupName = selectedGroup.value;
        let selectedGroupType = selectedGroup.getAttribute("group-type");

        // Get clicked list items attributes
        let itemType = li.getAttribute("item-type");
        let itemName = li.textContent;

        // ------------------- //
        // ------- ADD ------- //
        // ------------------- //
        /* Yields true if user clicks on source list item and
            it matches user list's group type */
        if (itemType === "source-row" && selectedGroupType === "row") {

            console.log("Adding item: '%s' to '%s'", itemName, selectedGroupName);

            gm.addItemToRowGroup(itemName, selectedGroupName);
        }
        else if (itemType === "source-col" && selectedGroupType === "col") {
            console.log("Adding item: '%s' to '%s'", itemName, selectedGroupName);

            gm.addItemToColGroup(itemName, selectedGroupName);
        }

        // -------------------- //
        // ------ REMOVE ------ //
        // -------------------- //
        //  Get selected tab
        let selectedTab = document.getElementsByClassName("nav-link active")[0].id;
        console.log("Selected tab: " + selectedTab);
        console.log("Item type: " + itemType);

        /* Yields true if user clicks on user list item and
        user list and selected tab are the same type */
        if (itemType === "user-row" && selectedTab === "row-tab") {
            console.log("Removing item: '%s' from '%s'", itemName, selectedGroupName);

            gm.removeItemFromRowGroup(itemName, selectedGroupName);
        }
        else if (itemType === "user-col" && selectedTab === "col-tab") {
            console.log("Removing item: '%s' from '%s'", itemName, selectedGroupName);

            gm.removeItemFromColGroup(itemName, selectedGroupName);
        }
        // Defined below
        updateLists();
    };
}

function updateSourceLists() {
    /*
     * Updates these source row and column lists according to
     * gm.sourceRows, gm.sourceCols
     * gm is GroupManager object constructed with blueprint
     * that comes from server
    */

    // Updates List Element
    const updateListElement = function(items, parent, itemType) {
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
            li.setAttribute("item-type", itemType);
            addOnclickFunctionToListItem(li);

            parent.appendChild(li);
        }
    };

    let sourceRowsList = document.getElementById("source-rows-list")
    let sourceColsList = document.getElementById("source-cols-list")

    updateListElement(gm.sourceRows, sourceRowsList, "source-row");
    updateListElement(gm.sourceCols, sourceColsList, "source-col");
}

function updateUserList() {
    // Render User List according to user's group selection

    // get which group is selected
    let selectElement = document.getElementById("user-group-select");
    let selected = selectElement.options[selectElement.selectedIndex];

    // Clear user list if nothing is selected or default option is selected
    if (selected === undefined || selected.id === "group-select-option-default") {
        // remove all children of user list
        let userList = document.getElementById("user-list");
        while (userList.firstChild) {
            userList.removeChild(userList.firstChild);
        }
        return;
    }

    let groupName = selected.value;

    let groupItems = Array();
    let groupType = selected.getAttribute("group-type");

    // itemType is for identifying when user clicks on list item
    let itemType = "";
    // get selected groups type
    if (groupType === "row") {
        // if type is row-group
        groupItems = gm.getRowGroup(groupName);
        itemType = "user-row";
    }
    else if (groupType === "col") {
        // if type is col-group
        groupItems = gm.getColGroup(groupName);
        itemType = "user-col";
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
        li.setAttribute("item-type", itemType);
        addOnclickFunctionToListItem(li);

        // append new list items to user list
        userList.appendChild(li);
    }
}


export function updateGroupSelect(groupNameToBeSelected, groupTypeToBeSelected, selectDefault=false) {

    // If a create group event is calling this function, the calling event will pass
    // the created groups name and type as arguments
    // so when user creates a group it will be auto selected

    // Else If a delete group event is calling this function,
    // updataGRoupSelect() will create the default option and auto select that.

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

    // generate new row options and append
    for (let i = 0; i < rowGroupNames.length; i++) {
        let itemName = rowGroupNames[i];

        let opt = document.createElement("option");
        opt.value = opt.textContent = itemName;

        if (groupTypeToBeSelected === "row" && itemName === groupNameToBeSelected) {
            console.log("Selected this group: " + opt.value + " || type: " + groupTypeToBeSelected);
            opt.selected = true;
        }
        opt.setAttribute("group-type", "row");

        groupSelect.appendChild(opt);
    }

    // append COLUMNS option
    groupSelect.appendChild(colClone);

    // generate new col options and append
    for (let i = 0; i < colGroupNames.length; i++) {
        let itemName = colGroupNames[i];

        let opt = document.createElement("option");
        opt.value = opt.textContent = itemName;
        if (groupTypeToBeSelected === "col" && itemName === groupNameToBeSelected) {
            console.log("Selected this group: " + opt.value + " || type: " + groupTypeToBeSelected);
            opt.selected = true;
        }
        opt.setAttribute("group-type", "col");

        groupSelect.appendChild(opt);
    }

    // select the option
    if (selectDefault == true) {
        // Create default option
        let defaultOption = document.createElement("option");
        defaultOption.id = "group-select-option-default";
        defaultOption.textContent = "USER GROUPS";
        defaultOption.hidden = true;
        defaultOption.selected = true;

        groupSelect.appendChild(defaultOption);
    }
}

export function updateLists() {
    updateSourceLists()
    updateUserList()
};