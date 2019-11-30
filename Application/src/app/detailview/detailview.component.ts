import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

export class documentData {
  title: string = "Empty Title";
  packages: Array<string> = [];
  keywords: Array<string> = [];

  constructor(title: string) {
    this.title = title;
  }
}

@Component({
  selector: 'app-detailview',
  templateUrl: './detailview.component.html',
  styleUrls: ['./detailview.component.scss']
})
export class DetailviewComponent implements OnInit {

  data: documentData = new documentData("Klausuraufgabe");

  documentForm = new FormGroup({
    title: new FormControl(''),
    packages: new FormControl(''),
    keywords: new FormControl(''),
  })

  constructor() {
   }

  ngOnInit() {
  }

}
