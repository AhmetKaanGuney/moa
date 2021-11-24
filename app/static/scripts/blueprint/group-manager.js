import { showErrorMessage } from "./errors.js"
// TODO later, mirror actions for rows and cols

class GroupManager {
    // source rows and cols are arrays of strings
    // user rows and cols are Objects {key: ["array-of-strings"]}
    constructor(blueprint) {
        this.sourceRows = blueprint.source.rows;
        this.sourceCols = blueprint.source.cols;
        this.userRowGroups = blueprint.user.rowGroups;
        this.userColGroups = blueprint.user.colGroups;
    }

    getRowGroup(groupName) {
        return this.userRowGroups[groupName];
    }

    getColGroup(groupName) {
        return this.userColGroups[groupName];
    }

    getBlueprint() {
        let blueprint = {
            "rows" :{},
            "cols" :{},
        };

        // Add user rows
        for (let row in this.userRowGroups) {
            blueprint.rows[row] = this.userRowGroups[row];
        }

        // add user cols
        for (let col in this.userColGroups) {
            blueprint.cols[col] = this.userColGroups[col];
        }
        return blueprint;
    }

    createRowGroup(name) {
        // Check if name is alredy in use
        if (name in this.userRowGroups) {
            showErrorMessage("Name: '" + name + "' already in use!");
            return;
        }
        else {
            this.userRowGroups[name] = Array();
        }
    }

    createColGroup(name) {
        if (name in this.userColGroups) {
            showErrorMessage("Name: '" + name + "' already in use!");
            return;
        }
        else {
            this.userColGroups[name] = Array();
        }
    }

    deleteRowGroup(name) {
        // Check if name exists
        let rowGroups = this.userRowGroups;
        if (name in rowGroups === false) {
            showErrorMessage("Group: '" + name + "' doesn't exists!");
            return;
        }
        let groupItems = rowGroups[name];
        for (let i = 0; i < groupItems.length; i++) {
            this.sourceRows.push(groupItems[i]);
        }
        console.log("Deleting: %s", name);
        delete rowGroups[name];
    }

    deleteColGroup(name) {
        let colGroups = this.userColGroups
        if (name in colGroups === false) {
            showErrorMessage("Group: '" + name + "' doesn't exists!");
            return;
        }
        let groupItems = colGroups[name];
        for (let i = 0; i < groupItems.length; i++) {
            this.sourceCols.push(groupItems[i]);
        }
        delete colGroups[name];
    }

    addItemToRowGroup(item, group) {
        // console.log(this.userRowGroups["test2"])
        this.userRowGroups[group].push(item);
        this.remove(item, this.sourceRows);
    }

    addItemToColGroup(item, group) {
        this.userColGroups[group].push(item);
        this.remove(item, this.sourceCols);
    }

    removeItemFromRowGroup(item, group) {
        let g = this.userRowGroups[group];
        this.remove(item, g);
        this.sourceRows.push(item);
    }

    removeItemFromColGroup(item, group) {
        let g = this.userColGroups[group];
        this.remove(item, g);
        this.sourceCols.push(item);
    }

    renameRowGroup(newName, oldName) {
        this.userRowGroups[newName] = this.getRowGroup(oldName);
        delete this.userRowGroups[oldName];
    }

    renameColGroup(newName, oldName) {
        this.userColGroups[newName] = this.getColGroup(oldName);
        delete this.userColGroups[oldName];
    }

    remove(item, list) {
        for (let i = 0; i < list.length; i++) {
            if (list[i] === item) {
                list.splice(i, 1);
            }
        }
    }

}

export {GroupManager}