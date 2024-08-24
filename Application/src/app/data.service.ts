import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { map } from 'rxjs/operators';
import { TeXDocument } from './model/texdocument';
import { InformationElement } from './model/informationElement';
import { ApiSpecs } from './config/app-config';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  url: string = ApiSpecs.uri;

  private TexDocuments: Array<TeXDocument>;
  public subject: BehaviorSubject<Array<TeXDocument>>;
  
  public TexDocumentSpecifications: Array<InformationElement>;

  constructor(private http: HttpClient) { 
    this.TexDocuments = [];
    this.subject = new BehaviorSubject(this.TexDocuments);
  }

  public getInformationTypeMap(): Observable<Object> {
    return this.http.get(this.url + ApiSpecs.getInformationTypeMap);
  }

  public getContentObjectSpecifications(contentObjectType: string = "TexDocument"): Observable<Array<InformationElement>> {
    return this.http.post(this.url + ApiSpecs.getContentObjectSpecifications, {"content_object_type": contentObjectType}).pipe(map(data => this.JsonToSpecificationArray(data["specifications"])));
  }

  public getInformationTypes(): Array<string> {
    let informationTypes: Array<string> = [];

    for (let spec of this.TexDocumentSpecifications) {
      informationTypes.push(spec.label);
    }

    return informationTypes;
  }

  /**
   * Converts a JSON with integers as keys into an array (1, 2, 3, ...) must be subsequent integers starting at 1.
   * The JSON itself has two entries, "entries" and "totalResultCount".
   * The list values have to be stored in "entries".
   * @param data Must provide an entry totalResultCount, reflecting the amount of elements
   */
  public JsonToArray(data: Object): Array<any> { // ToDo: make this generic!
    let outputArray: Array<any> = [];
    for (let i = 0; i < data[ApiSpecs.dataKeys.totalResultCount]; i++) {
      outputArray.push(data[ApiSpecs.dataKeys.entries][i]);
    }
    return outputArray;
  }

  private JsonToSpecificationArray(data: Object): Array<InformationElement> {
    let specsArray: Array<InformationElement> = [];

    for (let key of Object.keys(data)) {
      if (data[key]['label'] != 'Keywords' && data[key]['label'] != 'Packages') { //temporary! need to ship a version with some working features!
        specsArray.push(new InformationElement(data[key]['label'], data[key]['dataType'], '', data[key]["mandatory"], data[key]["array"]));
      }
    }

    return specsArray;
  }

  public getTexDocumentSpecifications(): Observable<Array<InformationElement>> {
    return this.http.get(this.url + ApiSpecs.getTexDocumentSpecifications).pipe(map(data => this.JsonToSpecificationArray(data)));
  }

  public getTexDocumentEntries(pageIndex: number = 1, pageSize: number = 5, filterValue: string = ""): Observable<Object> {
    let startAt: number = pageIndex * pageSize + 1;
    let maxResults: number = pageSize;
    if (typeof(filterValue) != "string") {
      console.warn("filterValue only accepts values of type string! Setting filterValue to the empty string.")
      filterValue = ""
    }
    let params: HttpParams = new HttpParams()
                                .set('startAt', startAt.toString())
                                .set('maxResults', maxResults.toString())
                                .set('filterValue', filterValue);
    return this.http.get(this.url + ApiSpecs.getTexDocumentEntries,  {
      params: params
                        }).pipe(map(res => {
                          return res['entries'];
                        }));
  }

  public addNewTexDocument(formData: FormData): Observable<Object> {
    return this.http.post(this.url + ApiSpecs.addTexDocumentEntry, formData);
  }

  public addNewContentObject(formData: FormData, contentObjectType: string): Observable<boolean> {
    return this.http.post(this.url + ApiSpecs.addContentObject, {
      formData: formData,
      type: contentObjectType,
      user: "admin"
    }).pipe(map(answer => {
      return answer["success"];
    }));
  }

  public editTexDocument(formData: FormData): void {
    let obs = this.http.post(this.url + ApiSpecs.editTexDocumentEntry, formData);
    obs.subscribe(data => {
      console.log(data);
    });
  }

  public editContentObject(formData: FormData, contentObjectType: string, Id: number): Observable<boolean> {
    return this.http.post(this.url + ApiSpecs.editContentObject, {
      formData: formData,
      Id: Id,
      type: contentObjectType,
      user: "admin"
    }).pipe(map(answer => {
      return answer["success"];
    }));
  }
}
