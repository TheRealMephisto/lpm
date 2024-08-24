import { Component } from '@angular/core';
import { TeXDocument } from './model/texdocument';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  # ToDo: use a string from a configuration file instead
  title = 'LaTeX Project Manager';

  public selectedDoc: TeXDocument = undefined;

  public viewCompiler: boolean;
  public viewEditor: boolean;

  ngOnInit() {
    this.viewCompiler = true;
    this.viewEditor = false;
  }

  public selectionChanged(event) {
    this.selectedDoc = event;
    this.viewCompiler = !this.selectedDoc;
  }

  public backToCompiler() {
    this.viewCompiler = true;
  }

  public showEditor(neu: string = '') {
    if (neu == 'new') {
      this.selectedDoc = undefined;
    }
    this.viewEditor = true;
  }

  public finishedDocumentEdit() {
    this.viewEditor = false;
  }
}
