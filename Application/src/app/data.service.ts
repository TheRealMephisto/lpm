import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataService {

  url: string = 'http://127.0.0.1:1337';

  constructor(private http: HttpClient) { }

  public addNewContent() {
    console.log("Hi! I'm here!");
    //console.log(this.http.get(this.url + '/addEntry'));
    this.http.get(this.url + '/addEntry')
  }
}
