import { Component } from '@angular/core';
import { TeXDocument } from './model/texdocument';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Application';

  selectedDoc: TeXDocument;

  viewCompiler: boolean;
  viewEditor: boolean;

  ngOnInit() {
    this.viewCompiler = true;
    this.viewEditor = false;
  }

  public selectDocument(event) {
    this.selectedDoc = event;
    this.viewCompiler = false;
  }

  public backToCompiler() {
    this.viewCompiler = true;
  }

  public showEditor() {
    this.viewEditor = true;
  }

  public finishedDocumentEdit() {
    this.viewEditor = false;
  }
}
