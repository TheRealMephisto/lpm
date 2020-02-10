import { Component, OnInit, ViewChild, Output, Input, EventEmitter, SimpleChange } from '@angular/core';

import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { map, startWith } from 'rxjs/operators';
import { MatTableDataSource, MatPaginator } from '@angular/material';
import { trigger, state, style, animate, transition } from '@angular/animations';

import { sampleExercises } from '../sample-data';
import { TeXDocument } from '../texdocument';
import { DataService } from '../data.service';

export interface PeriodicElement {
  title: string;
  version: number;
  creationDate: string;
}


const ELEMENT_DATA: PeriodicElement[] = [
  { title : sampleExercises[0].title,
    version: sampleExercises[0].version,
    creationDate: sampleExercises[0].getDateString()
  },
  { title : sampleExercises[1].title,
    version: sampleExercises[1].version,
    creationDate: sampleExercises[1].getDateString()
  },
  { title : sampleExercises[2].title,
    version: sampleExercises[2].version,
    creationDate: sampleExercises[2].getDateString()
  },
];

@Component({
  selector: 'app-explorer',
  templateUrl: './explorer.component.html',
  styleUrls: ['./explorer.component.scss'],
  animations: [
    trigger('detailExpand', [
      state('collapsed', style({height: '0px', minHeight: '0', display: 'none'})),
      state('expanded', style({height: '*'})),
      transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
    ]),
  ],
})
export class ExplorerComponent implements OnInit {

  @Input() selectedDocument: TeXDocument;
  @Output() selectedDocumentChange: EventEmitter<TeXDocument> = new EventEmitter<TeXDocument>();

  explorerFormControl = new FormControl();

  displayedColumns: string[] = ['title', 'version', 'creationDate'];
  dataSource = new MatTableDataSource<PeriodicElement>(ELEMENT_DATA);
  expandedElement: PeriodicElement | null;

  selectedRow: PeriodicElement | null;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator; // static: true -> make it available during ngOnInit

  constructor(private dataService: DataService) { }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
    console.log(filterValue);
  }

  ngOnChange(change: SimpleChange) {
    console.log(change);
  }

  public onClick(row) {
    this.selectedRow = this.selectedRow === row ? null : row;
    let selectedDocument = sampleExercises.find((x) => x.title == this.selectedRow.title && x.version == this.selectedRow.version);
    this.selectedDocumentChange.emit(selectedDocument);
  }

  public addNewContent() {
    console.log("button pressed, asking dataService to add content")
    this.dataService.addNewContent();
  }

}
