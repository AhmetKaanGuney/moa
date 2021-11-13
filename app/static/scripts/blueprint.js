// TODO let goo

// Selects
var sourceGroupsSelect = document.getElementById("source-groups-select")
var userGroupsSelect = document.getElementById("user-groups-select")

// Source and User Select Default Options
var sourceOptionRows = document.getElementById("soruce-option-rows")
var sourceOptionCols = document.getElementById("source-option-cols")

var userOptionRows = document.getElementById("user-option-rows")
var userOptionCols = document.getElementById("user-option-cols")

// Source Lists
var sourceRowsList = document.getElementById("source-rows-list")
var sourceColsList = document.getElementById("source-cols-list")

// User Lists
var userRowsList = document.getElementById("user-rows-list")
var userColsList = document.getElementById("user-Cols-list")

console.log(blueprint)

blueprint.rows["ahmet"] = 1

for (let element in blueprint) {
    console.log(element + ":")
    console.log(blueprint[element])
}

console.log(blueprint["rows"]["ahmet"])
console.log(blueprint.rows["ahmet"])