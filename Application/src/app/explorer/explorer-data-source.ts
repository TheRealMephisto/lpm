import { CollectionViewer, DataSource } from "@angular/cdk/collections";
import { BehaviorSubject, Observable, of } from 'rxjs';
import { DataService } from '../data.service';
import { TeXDocument } from '../model/texdocument';
import { TeXPackage } from '../model/texpackage';
import { ApiSpecs } from '../config/app-config';
import { catchError, finalize } from 'rxjs/operators';
import { InformationElement } from '../model/informationElement';

export class ExplorerDataSource implements DataSource<TeXDocument> {

    private TexDocumentSubject = new BehaviorSubject<Array<TeXDocument>>([]);
    private loadingSubject = new BehaviorSubject<boolean>(false);

    private numberOfPagesSubject = new BehaviorSubject<number>(1);
    public numberOfPages$ = this.numberOfPagesSubject.asObservable();

    // private TexDocumentSpecifications = new Array<InformationElement>();

    public TexDocuments$ = this.TexDocumentSubject.asObservable();
    public loading$ = this.loadingSubject.asObservable();

    constructor (private dataService: DataService) {
      // this.dataService.getTexDocumentSpecifications().subscribe((specifications: Array<InformationElement>) => {
      //   this.TexDocumentSpecifications = specifications;
      //   console.log('datasource: ', specifications);
      // });
      // this.TexDocumentSpecifications = this.dataService.TexDocumentSpecifications;
    }

    public connect(collectionViewer: CollectionViewer): Observable<TeXDocument[] | readonly TeXDocument[]> {
        return this.TexDocumentSubject.asObservable();
    }

    public disconnect(collectionViewer: CollectionViewer): void {
        this.TexDocumentSubject.complete();
        this.loadingSubject.complete();
    }

    public loadTexDocuments(pageIndex: number, pageSize: number = 5, filterValue: string = '') {
        this.loadingSubject.next(true);

        this.dataService.getTexDocumentEntries(pageIndex, pageSize, filterValue).pipe(
            catchError(() => of([])),
            finalize(() => this.loadingSubject.next(false))
        )
        .subscribe((entries: Object) => {
          let texDocuments: Array<TeXDocument> = [];

          for (let i = 1; i <= pageSize; i++) {
            if (entries[i]) {
              texDocuments.push(new TeXDocument(entries[i]))
            }
          }

          this.numberOfPagesSubject.next(entries[ApiSpecs.dataKeys.totalTableContentCount]);

          this.TexDocumentSubject.next(texDocuments);
        });
    }

}