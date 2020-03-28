import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { TeXDocument } from './model/texdocument';
import { TeXPackage } from './model/texpackage';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  url: string = 'http://127.0.0.1:1337/api';

  private TexDocuments: Array<TeXDocument>;
  public subject: BehaviorSubject<Array<TeXDocument>>;

  constructor(private http: HttpClient) { 
    this.TexDocuments = [];
    this.subject = new BehaviorSubject(this.TexDocuments);
  }

  public getInformationTypes(): Observable<Object> {
    return this.http.get(this.url + '/getInformationTypes');
  }

  /**
   * Converts a JSON with integers as keys into an array (1, 2, 3, ...) must be subsequent integers starting at 1.
   * The JSON itself has two entries, "entries" and "totalResultCount".
   * The list values have to be stored in "entries".
   * @param data Must provide an entry totalResultCount, reflecting the amount of elements
   */
  public JsonToArray(data: Object): Array<any> { // ToDo: make this generic!
    let outputArray: Array<any> = [];
    for (let i = 0; i < data['totalResultCount']; i++) {
      outputArray.push(data['entries'][i]);
    }
    return outputArray;
  }

  private JsonToTeXDocument(dataEntry: Object): TeXDocument {
    let packages: Array<TeXPackage> = [];
    for (let i = 0; i < dataEntry['packagesCount']; i++) {
      let packageName: string = dataEntry['packages'][i]['package'];
      let packageOptions: Array<string> = [];
      for (let j = 0; j < dataEntry['packages'][i]['optionsCount']; j++) {
        packageOptions.push(dataEntry['packages'][i]['options'][j]);
      }
      packages.push(new TeXPackage(packageName, packageOptions));
    }

    let texDocument: TeXDocument = new TeXDocument(
      "",
      dataEntry['title'],
      0, // provide version, not information in JSON sent from API!
      new Date(dataEntry['creationDate']),
      [""], // provide keywords, not information in JSON sent from API!
      packages,
      "",
      ""
    );
    return texDocument;
  }

  public getTexDocumentEntries(startAt: number, maxResults: number): void {
    let params: HttpParams = new HttpParams()
                                .set('startAt', startAt.toString())
                                .set('maxResults', maxResults.toString());
    let request = this.http.get(this.url + '/getTexDocumentEntries', {
      params: params
    });
    request.subscribe(data => {
      this.TexDocuments = [];
      for (let i = 1; i <= data['entries']['totalResultCount']; i++) {
        this.TexDocuments.push(this.JsonToTeXDocument(data["entries"][i]));
        this.subject.next(this.TexDocuments);
      }
    });
    return;
  }

  public addNewTexDocument(formData: FormData): void {
    let obs = this.http.post(this.url + '/addTexDocumentEntry', formData);
    obs.subscribe(data => {
      console.log(data);
    });
  }
}
