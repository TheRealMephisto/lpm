import { SelectionModel } from '@angular/cdk/collections';
import { FlatTreeControl } from '@angular/cdk/tree';
import { Component, Input, OnInit } from '@angular/core';
import { MatTreeFlatDataSource, MatTreeFlattener } from '@angular/material/tree';
import { TreeviewDatabase } from './treeview-database';
import { PackageFlatNode } from './package-flat-node';
import { PackageNode } from './package-node';

// This code is mostly one of the examples avaible on the official angular material web page!
// It probably needs some changes to adjust my specific needs!

/**
 * @title Tree with checkboxes
 */
@Component({
  selector: 'package-options-treeview',
  templateUrl: './package-options-treeview.component.html',
  styleUrls: ['./package-options-treeview.component.scss'],
  providers: [TreeviewDatabase]
})
export class PackageOptionsTreeviewComponent implements OnInit {

  @Input() treeData: JSON;

  /** Map from flat node to nested node. This helps us finding the nested node to be modified */
  flatNodeMap = new Map<PackageFlatNode, PackageNode>();

  /** Map from nested node to flattened node. This helps us to keep the same object for selection */
  nestedNodeMap = new Map<PackageNode, PackageFlatNode>();

  /** A selected parent node to be inserted */
  selectedParent: PackageFlatNode | null = null;

  /** The new item's name */
  newItemName = '';

  treeControl: FlatTreeControl<PackageFlatNode>;

  treeFlattener: MatTreeFlattener<PackageNode, PackageFlatNode>;

  dataSource: MatTreeFlatDataSource<PackageNode, PackageFlatNode>;

  /** The selection for checklist */
  checklistSelection = new SelectionModel<PackageFlatNode>(true /* multiple */);

  constructor(private _database: TreeviewDatabase) {  }

  ngOnInit(): void {
    this._database.initialize(this.treeData);
    this.treeFlattener = new MatTreeFlattener(this.transformer, this.getLevel,
      this.isExpandable, this.getChildren);
    this.treeControl = new FlatTreeControl<PackageFlatNode>(this.getLevel, this.isExpandable);
    this.dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);

    this._database.dataChange.subscribe(data => {
      this.dataSource.data = data;
    });
  }

  getLevel = (node: PackageFlatNode) => node.level;

  isExpandable = (node: PackageFlatNode) => node.expandable;

  getChildren = (node: PackageNode): PackageNode[] => node.children;

  hasChild = (_: number, _nodeData: PackageFlatNode) => _nodeData.expandable;

  hasNoContent = (_: number, _nodeData: PackageFlatNode) => _nodeData.item === '';

  /**
   * Transformer to convert nested node to flat node. Record the nodes in maps for later use.
   */
  transformer = (node: PackageNode, level: number) => {
    const existingNode = this.nestedNodeMap.get(node);
    const flatNode = existingNode && existingNode.item === node.item
        ? existingNode
        : new PackageFlatNode();
    flatNode.item = node.item;
    flatNode.level = level;
    flatNode.expandable = !!node.children;
    this.flatNodeMap.set(flatNode, node);
    this.nestedNodeMap.set(node, flatNode);
    return flatNode;
  }

  /** Whether all the descendants of the node are selected. */
  descendantsAllSelected(node: PackageFlatNode): boolean {
    const descendants = this.treeControl.getDescendants(node);
    const descAllSelected = descendants.every(child =>
      this.checklistSelection.isSelected(child)
    );
    return descAllSelected;
  }

  /** Whether part of the descendants are selected */
  descendantsPartiallySelected(node: PackageFlatNode): boolean {
    const descendants = this.treeControl.getDescendants(node);
    const result = descendants.some(child => this.checklistSelection.isSelected(child));
    return result && !this.descendantsAllSelected(node);
  }

  /** Toggle the to-do item selection. Select/deselect all the descendants node */
  PackageSelectionToggle(node: PackageFlatNode): void {
    this.checklistSelection.toggle(node);
    const descendants = this.treeControl.getDescendants(node);
    this.checklistSelection.isSelected(node)
      ? this.checklistSelection.select(...descendants)
      : this.checklistSelection.deselect(...descendants);

    // Force update for the parent
    descendants.every(child =>
      this.checklistSelection.isSelected(child)
    );
    this.checkAllParentsSelection(node);
  }

  /** Toggle a leaf to-do item selection. Check all the parents to see if they changed */
  todoLeafItemSelectionToggle(node: PackageFlatNode): void {
    this.checklistSelection.toggle(node);
    this.checkAllParentsSelection(node);
  }

  /* Checks all the parents when a leaf node is selected/unselected */
  checkAllParentsSelection(node: PackageFlatNode): void {
    let parent: PackageFlatNode | null = this.getParentNode(node);
    while (parent) {
      this.checkRootNodeSelection(parent);
      parent = this.getParentNode(parent);
    }
  }

  /** Check root node checked state and change it accordingly */
  checkRootNodeSelection(node: PackageFlatNode): void {
    const nodeSelected = this.checklistSelection.isSelected(node);
    const descendants = this.treeControl.getDescendants(node);
    const descAllSelected = descendants.every(child =>
      this.checklistSelection.isSelected(child)
    );
    if (nodeSelected && !descAllSelected) {
      this.checklistSelection.deselect(node);
    } else if (!nodeSelected && descAllSelected) {
      this.checklistSelection.select(node);
    }
  }

  /* Get the parent node of a node */
  getParentNode(node: PackageFlatNode): PackageFlatNode | null {
    const currentLevel = this.getLevel(node);

    if (currentLevel < 1) {
      return null;
    }

    const startIndex = this.treeControl.dataNodes.indexOf(node) - 1;

    for (let i = startIndex; i >= 0; i--) {
      const currentNode = this.treeControl.dataNodes[i];

      if (this.getLevel(currentNode) < currentLevel) {
        return currentNode;
      }
    }
    return null;
  }

  /** Select the category so we can insert the new item. */
  addNewItem(node: PackageFlatNode) {
    const parentNode = this.flatNodeMap.get(node);
    this._database.insertItem(parentNode!, '');
    this.treeControl.expand(node);
  }

  /** Save the node to database */
  saveNode(node: PackageFlatNode, itemValue: string) {
    const nestedNode = this.flatNodeMap.get(node);
    this._database.updateItem(nestedNode!, itemValue);
  }
}