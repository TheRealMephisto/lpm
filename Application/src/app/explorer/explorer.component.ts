import { Component, OnInit, ViewChild, Output, Input, EventEmitter, SimpleChange, ChangeDetectorRef } from '@angular/core';

import { FormControl } from '@angular/forms';
import { MatTableDataSource, MatPaginator } from '@angular/material';
import { trigger, state, style, animate, transition } from '@angular/animations';

import { sampleExercises } from '../sample-data';
import { TeXDocument } from '../model/texdocument';
import { DataService } from '../data.service';
import { Observable } from 'rxjs';
import { PeriodicElement } from '../periodic-elements';



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
  // changeDetection: ChangeDetectionStrategy.OnPU
})
export class ExplorerComponent implements OnInit {

  @Input() selectedDocument: TeXDocument;
  @Output() selectedDocumentChange: EventEmitter<TeXDocument> = new EventEmitter<TeXDocument>();
  @Output() addDocument: EventEmitter<any> = new EventEmitter<any>();

  explorerFormControl = new FormControl();

  displayedColumns: string[] = ['title', 'version', 'creationDate'];
  dataSourceObs: Observable<Object>;
  dataSource: MatTableDataSource<PeriodicElement> = new MatTableDataSource<PeriodicElement>(ELEMENT_DATA);
  expandedElement: PeriodicElement | null;

  selectedRow: PeriodicElement | null;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator; // static: true -> make it available during ngOnInit

  constructor(
    private dataService: DataService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;
    this.dataService.subject.subscribe((TeXDocuments: Array<TeXDocument>) => {
      this.dataSource = new MatTableDataSource<PeriodicElement>(this.TeXDocumentsToPeriodicElementsArray(TeXDocuments));
      this.cdr.detectChanges();
    });
    this.dataService.getTexDocumentEntries(1, 3);
  }

  private TeXDocumentsToPeriodicElementsArray(TeXDocuments: Array<TeXDocument>): Array<PeriodicElement> {
    let outputArray: Array<PeriodicElement> = [];
    for (const texDoc of TeXDocuments) {
      outputArray.push({
        title : texDoc.title,
        version: texDoc.version,
        creationDate: texDoc.creationDate.toString()
      });
    }
    return;
  }

  applyFilter(filterValue: string) {
    this.dataSource.filter = filterValue.trim().toLowerCase();
    console.log(filterValue);
  }

  ngOnChange(change: SimpleChange) {
    console.log(change);
  }

  public addDocumentTrigger() {
    this.addDocument.emit();
  }

  public onClick(row) {
    this.selectedRow = this.selectedRow === row ? null : row;
    let selectedDocument = sampleExercises.find((x) => x.title == this.selectedRow.title && x.version == this.selectedRow.version);
    this.selectedDocumentChange.emit(selectedDocument);
  }
}
