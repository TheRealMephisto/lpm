import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { PackageNode } from './package-node';

/**
 * Treeview database, it can build a tree structured Json object.
 * If a node is a category, it has children items and new items can be added under the category.
 */
@Injectable()
export class TreeviewDatabase {
  dataChange = new BehaviorSubject<PackageNode[]>([]);

  treeData;

  get data(): PackageNode[] { return this.dataChange.value; }

  constructor() { }

  public initialize( treeData ) {
    this.treeData = treeData;
    // Build the tree nodes from Json object. The result is a list of `PackageNode` with nested
    //     file node as children.
    const data = this.buildFileTree(this.treeData, 0);

    // Notify the change.
    this.dataChange.next(data);
  }

  /**
   * Build the file structure tree. The `value` is the Json object, or a sub-tree of a Json object.
   * The return value is the list of `PackageNode`.
   */
  buildFileTree(obj: {[key: string]: any}, level: number): PackageNode[] {
    return Object.keys(obj).reduce<PackageNode[]>((accumulator, key) => {
      const value = obj[key];
      const node = new PackageNode();
      node.item = key;

      if (value != null) {
        if (typeof value === 'object') {
          node.children = this.buildFileTree(value, level + 1);
        } else {
          node.item = value;
        }
      }

      return accumulator.concat(node);
    }, []);
  }
  
  /** Add an item to to-do list */
  insertItem(parent: PackageNode, name: string) {
    if (parent.children) {
      parent.children.push({item: name} as PackageNode);
      this.dataChange.next(this.data);
    }
  }

  updateItem(node: PackageNode, name: string) {
    node.item = name;
    this.dataChange.next(this.data);
  }
}