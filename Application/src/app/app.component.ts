import { Component } from '@angular/core';
import { TeXDocument } from './texdocument';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Application';

  selectedDoc: TeXDocument;

  viewCompiler: boolean;

  ngOnInit() {
    this.viewCompiler = true;
  }

  public selectDocument(event) {
    this.selectedDoc = event;
    this.viewCompiler = false;
  }

  public backToCompiler() {
    this.viewCompiler = true;
  }
}
