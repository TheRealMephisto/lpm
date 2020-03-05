import { Component, OnInit, Input, SimpleChange } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { TeXDocument } from '../model/texdocument';

@Component({
  selector: 'app-detailview',
  templateUrl: './detailview.component.html',
  styleUrls: ['./detailview.component.scss']
})
export class DetailviewComponent implements OnInit {

  @Input() selectedDocument: TeXDocument;

  documentForm = new FormGroup({
    title: new FormControl(''),
    packages: new FormControl(''),
    keywords: new FormControl(''),
  })

  constructor() {
   }

  ngOnInit() {
  }

  ngOnChange(change: SimpleChange) {
    console.log(change);
  }

  compile() {
    console.log(this.selectedDocument);
  }

  openTexFile() {
    console.log(this.selectedDocument.rawDataPath);
    window.open(this.selectedDocument.rawDataPath, "_blank");
  }

  openPdfFile() {
    window.open(this.selectedDocument.outputPath, "_blank")
  }

}
