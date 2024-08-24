import {
  Component,
  OnInit,
  OnChanges,
  ViewChild,
  Output,
  Input,
  EventEmitter,
  SimpleChanges,
  ChangeDetectionStrategy,
  ChangeDetectorRef } from '@angular/core';
import { FormControl } from '@angular/forms';
import {
  MatPaginator,
  PageEvent } from '@angular/material';
import {
  trigger,
  state,
  style,
  animate,
  transition } from '@angular/animations';
import { TeXDocument } from '../model/texdocument';
import { DataService } from '../data.service';
import { Observable } from 'rxjs';
import { ExplorerDataSource } from './explorer-data-source';

// ToDo: For implementation of a loading indicator: https://blog.angular-university.io/angular-material-data-table/

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
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ExplorerComponent implements OnInit, OnChanges {

  @Input() selectedDocument: TeXDocument;
  @Output() selectedDocumentChange: EventEmitter<TeXDocument> = new EventEmitter<TeXDocument>();
  @Output() addDocument: EventEmitter<any> = new EventEmitter<any>();

  public pageSize: number = 5;

  public currentPageIndex: number = 0;

  public length: number;

  public explorerFormControl = new FormControl();

  displayedColumns: string[] = ['title', 'version', 'creationDate'];
  dataSourceObs: Observable<Object>;

  public dataSource: ExplorerDataSource ;

  expandedElement: TeXDocument | null;

  selectedRow: TeXDocument | null;

  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  constructor(
    private dataService: DataService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.dataSource = new ExplorerDataSource(this.dataService);
    this.dataSource.TexDocuments$.subscribe(objects => {
      this.changeSelection(objects[0]);
    });
    this.dataSource.loadTexDocuments(0);
    this.dataSource.numberOfPages$.subscribe(n => {
      this.length = n;
      this.cdr.detectChanges();
    });
  }

  applyFilter() {
    this.executePaginationEvent(0, this.pageSize);
  }

  //  ngOnChanges(change: SimpleChanges) {
    // console.log('Changes in explorer component: ', change);
  //  }

  public executePaginationEvent(pageIndex: number, pageSize: number): void {
    this.currentPageIndex = pageIndex;
    this.pageSize = pageSize;
    this.dataSource.loadTexDocuments(pageIndex, pageSize, this.explorerFormControl.value);
  }

  public paginationEventHandler(event: PageEvent): void {
    this.executePaginationEvent(event.pageIndex, event.pageSize)
  }

  public addDocumentTrigger() {
    this.addDocument.emit();
  }

  public changeSelection(row: TeXDocument) {
    this.selectedRow = (this.selectedRow === row) ? undefined : row;
    this.selectedDocumentChange.emit(this.selectedRow);
  }
}
