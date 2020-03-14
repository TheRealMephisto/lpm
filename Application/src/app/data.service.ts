import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  url: string = 'http://127.0.0.1:1337/api';

  constructor(private http: HttpClient) { }

  public getTexDocumentEntries(startAt: number, maxResults: number) {
    let params: HttpParams = new HttpParams()
                                .set('startAt', startAt.toString())
                                .set('maxResults', maxResults.toString());
    console.log("params: ", params);
    let request = this.http.get(this.url + '/getTexDocumentEntries', {
      params: params
    });
    request.subscribe(data => {
      console.log(data);
    });
  }

  public addNewTexDocument(formData: FormData): void {
    console.log("DataServive: ", formData);
    console.log(typeof(formData));

    // ToDo: rewrite API to directly accept JSON

    let filePathList: string = "AwesomeFilePath1,AwesomeFilePath2";
    let informationList: string = "AwesomeInfo1,AwesomeInfo2";
    let informationTypeList: string = "AwesomeInfoType1,AwesomeInfoType2";
    let packageList: string = "AwesomePackage1,AwesomePackage2";
    let packageOptionsList: string = "AwesomeOpt1,AwesomeOpt2,AwesomeOpt3;AwesomeOpt3,AwesomeOpt4";

    let params: HttpParams = new HttpParams()
                                .set('title', formData['title'])
                                .set('path', formData['path'])
                                .set('username', formData['username'])
                                .set('filePathList', filePathList)
                                .set('informationList', informationList)
                                .set('informationTypeList', informationTypeList)
                                .set('packageList', packageList)
                                .set('packageOptionsList', packageOptionsList);
    console.log("params: ", params);
    let obs = this.http.get(this.url + '/addTexDocumentEntry', {
      params: params
    });
    obs.subscribe(data => {
      console.log(data);
    });
    
  }

  public addNewContent(): void {
    let title: string = "AwesomeTitle";
    let path: string = "AwesomePath";
    let username: string = "AwesomeName";
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
    console.log("params: ", params);
    let obs = this.http.get(this.url + '/addTexDocumentEntry', {
      params: params
    });
    obs.subscribe(data => {
      console.log(data);
    });
  }
}
