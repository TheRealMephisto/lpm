import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { strict } from 'assert';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  url: string = 'http://127.0.0.1:1337/api';

  constructor(private http: HttpClient) { }

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
    for (let i = 1; i <= data['totalResultCount']; i++) {
      outputArray.push(data['entries'][i]);
    }
    return outputArray;
  }

  public getTexDocumentEntries(startAt: number, maxResults: number): Observable<Object> {
    let params: HttpParams = new HttpParams()
                                .set('startAt', startAt.toString())
                                .set('maxResults', maxResults.toString());
    let request = this.http.get(this.url + '/getTexDocumentEntries', {
      params: params
    });
    return request;
  }

  public addNewTexDocument(formData: FormData): void {

    let obs = this.http.post(this.url + '/addTexDocumentEntry', formData);
    obs.subscribe(data => {
      console.log(data);
    });
  }

  public addNewContent(): void {
    let title: string = "AwesomeTitle";
    let path: string = "AwesomePath";
    let username: string = "devUser";
    let filePathList: string = "AwesomeFilePath1,AwesomeFilePath2";
    let informationList: string = "AwesomeInfo1,AwesomeInfo2";
    let informationTypeList: string = "AwesomeInfoType1,AwesomeInfoType2";
    let packageList: string = "AwesomePackage1,AwesomePackage2";
    let packageOptionsList: string = "AwesomeOpt1,AwesomeOpt2,AwesomeOpt3;AwesomeOpt3,AwesomeOpt4";

    let params: HttpParams = new HttpParams()
                                .set('title', title)
                                .set('path', path)
                                .set('username', username)
                                .set('filePathList', filePathList)
                                .set('informationList', informationList)
                                .set('informationTypeList', informationTypeList)
                                .set('packageList', packageList)
                                .set('packageOptionsList', packageOptionsList);
    let obs = this.http.get(this.url + '/addTexDocumentEntry', {
      params: params
    });
    obs.subscribe(data => {
      console.log(data);
    });
  }
}
