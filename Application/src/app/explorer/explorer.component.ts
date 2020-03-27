import { Component, OnInit, ViewChild, Output, Input, EventEmitter, SimpleChange, ChangeDetectorRef } from '@angular/core';

import { FormControl } from '@angular/forms';
import { MatTableDataSource, MatPaginator } from '@angular/material';
import { trigger, state, style, animate, transition } from '@angular/animations';

import { TeXDocument } from '../model/texdocument';
import { DataService } from '../data.service';
import { Observable } from 'rxjs';

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
  @Output() addDocument: EventEmitter<any> = new EventEmitter<any>();

  explorerFormControl = new FormControl();

  displayedColumns: string[] = ['title', 'version', 'creationDate'];
  dataSourceObs: Observable<Object>;
  dataSource: MatTableDataSource<TeXDocument> = new MatTableDataSource<TeXDocument>();
  expandedElement: TeXDocument | null;

  selectedRow: TeXDocument | null;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator; // static: true -> make it available during ngOnInit

  constructor(
    private dataService: DataService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.dataSource.paginator = this.paginator;
    this.dataService.subject.subscribe((TeXDocuments: Array<TeXDocument>) => {
      this.dataSource = new MatTableDataSource<TeXDocument>(TeXDocuments);
    });
    this.dataService.getTexDocumentEntries(1, 3);
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

  public onClick(row: TeXDocument) {
    this.selectedRow = this.selectedRow === row ? null : row;
    this.selectedDocumentChange.emit(this.selectedRow);
  }
}
