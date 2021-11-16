// TODO later, mirror actions for rows and cols
// add, remove, create, delete, rename

class GroupManager {
    // source rows and cols are arrays of strings
    // user rows and cols are Objects {key: ["array-of-strings"]}
    constructor(blueprint) {
        this.sourceRows = blueprint.source.rows
        this.sourceCols = blueprint.source.cols
        this.userRowGroups = blueprint.user.rowGroups
        this.userColGroups = blueprint.user.colGroups
    }

    getRowGroup(groupName) {
        return this.userRowGroups[groupName]
    }

    getColGroup(groupName) {
        return this.userColGroups[groupName]
    }

    createRowGroup(name) {
        // Check if name is alredy in use
        if (name in this.userRowGroups) {
            console.log("Name: '%s' already in use!", name)
            return null
        }
        else {
            this.userRowGroups[name] = Array()
        }
    }

    createColGroup(name) {
        if (name in this.userColGroups) {
            console.log("Name: '%s' already in use!", name)
            return null
        }
        else {
            this.userRowGroups[name] = Array()
        }
    }

    deleteRowGroup(name) {
        // Check if name exists
        let rowGroups = this.userRowGroups
        if (name in rowGroups === false) {
            console.log("Group: '%s' doesn't exist!", name)
            return null
        }
        let groupItems = rowGroups[name]
        for (let i = 0; i < groupItems.length; i++) {
            this.sourceRows.push(groupItems[i])
        }
        console.log("Deleting: %s", name)
        delete rowGroups[name]
    }

    deleteColGroup(name) {
        let colGroups = this.userColGroups
        if (name in colGroups === false) {
            console.log("Group: '%s' doesn't exist!", name)
            return null
        }
        let groupItems = colGroups[name]
        for (let i = 0; i < groupItems.length; i++) {
            this.sourceCols.push(groupItems[i])
        }
        delete colGroups[name]
    }

    addToRowGroups(items, group) {
        // console.log(this.userRowGroups["test2"])
        for (let i = 0; i < items.length; i++) {
            this.userRowGroups[group].push(items[i])
            this.remove(items[i], this.sourceRows)
        }
    }

    addToColGroups(items, group) {
        for (let i = 0; i < items.length; i++) {
            this.userColGroups[group].push(items[i])
            this.remove(items[i], this.sourceCols)
        }
    }

    removeFromRowGroup(items, group) {
        let g = this.userRowGroups[group]

        for (let i = 0; i < items.length; i++) {
            this.remove(items[i], g)
            this.sourceRows.push(items[i])
        }
    }

    removeFromColGroup(items, group) {
        return
    }

    renameRowGroup(newName, groupName) {
        this.userRowGroups[newName] = this.getRowGroup(groupName)
        delete this.getRowGroup
    }

    renameColGroup(newName, groupName) {
        this.userColGroups[newName] = this.getColGroup(groupName)
        delete this.getColGroup
    }

    remove(item, list) {
        for (let i = 0; i < list.length; i++) {
            if (list[i] === item) {
                list.splice(i, 1)
            }
        }
    }
}

export {GroupManager}
