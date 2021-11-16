import { gm } from "./globals.js"

console.log("Source: ")
console.log(gm.sourceRows)
console.log("\n")

console.log("Create()")
gm.createRowGroup("test1")
gm.createRowGroup("test2")
gm.createRowGroup("test3")

console.log("User: ")
console.log(gm.userRowGroups)
console.log("\n")


console.log("Add()")
gm.addToRowGroups(["ali", "ahmet", "ibrahim"], "test2")

console.log("test2: ")
console.log(gm.userRowGroups["test2"])
console.log("Source: ")
console.log(gm.sourceRows)
console.log("\n")

console.log("Remove()")
gm.removeFromRowGroup(["ali", "ahmet"], "test2")

console.log("test2: ")
console.log(gm.userRowGroups["test2"])
console.log("Source: ")
console.log(gm.sourceRows)
console.log("\n")

console.log("Delete()")
gm.deleteRowGroup("test")
gm.deleteRowGroup("test2")

console.log("User: ")
console.log(gm.userRowGroups)
console.log("Source: ")
console.log(gm.sourceRows)
console.log("\n")