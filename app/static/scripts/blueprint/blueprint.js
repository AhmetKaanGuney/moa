import { GroupManager } from "./group-manager.js"

var init_happened = false

// Selects
var sourceGroupSelect = document.getElementById("source-groups-select")
var userGroupSelect = document.getElementById("user-groups-select")

// Source Lists
var sourceRowsList = document.getElementById("source-rows-list")
var sourceColsList = document.getElementById("source-cols-list")

// User Lists
var userList = document.getElementById("user-list")

var gm = new GroupManager(blueprint)
console.log("--- GroupManager ---")
console.log(gm)


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


// Assign onclick events
document.getElementById("create-group").onclick = function() {
    console.log("create group()")

    modifyModal("Create Group", "Group Name", "create")
    // Unhide row col select box
    document.getElementById("modal-group-type-select").hidden = false

    modalWindow.show()
}

document.getElementById("delete-group").onclick = function() {
    console.log("delete group ()")
}

document.getElementById("rename-group").onclick = function() {
    console.log("rename group()")

    modifyModal("Rename Group", "New Group Name", "rename")
    // Hide select box
    document.getElementById("modal-group-type-select").hidden = true
    modalWindow.show()
}

// Assign onlick events on multiple elements
var addButtons = document.getElementsByName("add-selected")
for (let i = 0; i < addButtons.length; i++) {
    addButtons[i].onclick = function() {
        console.log("add selected()")
    }
}

var removeButtons = document.getElementsByName("remove-selected")
for (let i = 0; i < removeButtons.length; i++) {
    removeButtons[i].onclick = function() {
        console.log("remove selected()")
    }
}


// Assign onclick to modalWindow's 'Okay' button
document.getElementById("modal-ok-button").onclick = function() {
    let action = document.getElementById("modal-ok-button").getAttribute("action")
    console.log("Action type %s", action)

    if (action === "create") {
        let inputValue = document.getElementById("modal-input").value
        let groupType = getSelectedValue(document.getElementById("modal-group-type-select"))

        if (groupType === "row") {
            gm.createRowGroup(inputValue)
        }

        if (groupType === "col") {
            gm.createColGroup(inputValue)
        }
    }

    if (action === "rename") {
        let selectedGroupName = getSelectedValue(userGroupSelect)

        if (groupType === "row") {
            gm.renameRowGroup(inputValue, selectedGroupName)
        }
    }
    console.log(gm)
    modalWindow.hide()
}

// Update User Group Select
function updateUserGroupSelect() {
    let options = userGroupSelect.options

    // Remove old options
    for (let i = 0; i < options.length; i++) {

        if (options[i].className === "disabled-option")
        {
            continue
        }

        userGroupSelect.remove(i)
    }
    // TODO Add rows between ROWS - COLS options
    // TODO Add col after COLS option

    // // Add new Options
    // for (let i = 0; i < gm.userRowGroups.length; i++) {

    //     groupName = gm.userRowGroups[i]

    //     // Create option
    //     let opt = document.createElement("option")
    //     opt.textContent = groupName

    // }
}

updateUserGroupSelect()
// check if default initialization happend
// if not trigger these events
if (!init_happened) {
    sourceGroupSelect.onchange()
    init_happened = true
}
