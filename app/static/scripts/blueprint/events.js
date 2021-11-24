import { gm } from "./globals.js";
import { showErrorMessage } from "./errors.js";
import { modalWindow, modifyModal } from "./modal-window.js";
import { updateLists, updateGroupSelect } from "./update.js";

/* Assign functions to button and call updateElements() on every button click */
// --------------------------- //
// ------- FUNCTIONS --------- //
// --------------------------- //
function postBlueprint(blueprint, fileFormat) {
    let data = {
        "blueprint": blueprint,
        "fileFormat": fileFormat
    }
    fetch("/blueprint.html", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(async response => {
        try {
            const response_data = await response.json();
            console.log("response data: ", response_data);
            if (response_data["status"] === "OK") {
                let url = response_data["download_url"];
                downloadFile(url);
            } else {
                console.log("ERROR detected")
                let errorMessage = response_data["error"];
                showErrorMessage(errorMessage);
            }
        } catch(error) {
            console.warn(error);
        }
    })
}

function downloadFile(url) {
    fetch(url).then(response => {
        const statusCode = response.status;
        if (statusCode === 404) {
            alert("An error occurred when downloading.");
        } else {
            let link = document.createElement("a");
            link.href = url;
            console.log("ANCHOR:", url)
            console.log(link)
            link.click();
            link.remove();
        }
    })
}

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
// DOWNLOAD MENU BUTTONS
// Dowload xlsx
document.getElementById("download-xlsx-button").onclick = function() {
    let blueprint = gm.getBlueprint();
    postBlueprint(blueprint, "xlsx");
}
// Download xls
document.getElementById("download-xls-button").onclick = function() {
    let blueprint = gm.getBlueprint();
    postBlueprint(blueprint, "xls");
}

// Download csv
document.getElementById("download-csv-button").onclick = function() {
    let blueprint = gm.getBlueprint();
    postBlueprint(blueprint, "csv");
}


// GROUP MENU BUTTONS
// CREATE GROUP
document.getElementById("create-group").onclick = createGroup;

// RENAME GROUP BUTTON
document.getElementById("rename-group").onclick = renameGroup;


// DELETE GROUP BUTTON
document.getElementById("delete-group").onclick = deleteGroup;

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