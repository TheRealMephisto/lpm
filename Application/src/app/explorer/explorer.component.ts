import { Component, OnInit } from '@angular/core';

import {FormControl, FormGroup} from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';

@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.scss']
})
export class ExplorerComponent implements OnInit {

  explorerFormControl = new FormControl();
  options: string[] = ['one', 'two', 'three'];
  filteredOptions: Observable<string[]>;

  items = [
    { title: "test1" },
    { title: "test2" },
    { title: "test3" }
  ];

  constructor() { }

  ngOnInit() {
    this.filteredOptions = this.explorerFormControl.valueChanges.pipe(
      startWith(''),
      map(value => this._filter(value))
    );
  }

  private _filter(value: string): string[] {
    const filterValue = value.toLowerCase();

    return this.options.filter(option => option.toLowerCase().indexOf(filterValue) === 0);
  }

}
