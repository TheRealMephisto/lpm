import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';

/**
 * Provide a form enabling the user to edit database entries, i.e. of TeX-Documents.
 */
@Component({
  selector: 'app-document-editor',
  templateUrl: './document-editor.component.html',
  styleUrls: ['./document-editor.component.scss']
})
export class DocumentEditorComponent implements OnInit {

  fileEnding: string = 'tex'

  constructor() { }

  ngOnInit() {
    this.author.setValue('devUser')
  }

  title = new FormControl('', [Validators.required]);
  path = new FormControl('', [Validators.required, Validators.pattern('.*\.'.concat(this.fileEnding))]);
  author = new FormControl('', [Validators.required]);

  getErrorMessage(target: string): string {
    let targetForm: FormControl;
    switch(target) {
      case 'title':
        targetForm = this.title;
        break;
      case 'path':
        targetForm = this.path;
        break;
      case 'author':
        targetForm = this.author;
        break;
      default:
        return;
    }
    if (targetForm.hasError('required')) {
      return 'You must enter a value';
    }
    if (targetForm.hasError('pattern')) {
      return 'Must be a file path ending on .'.concat(this.fileEnding);
    }
  }

}
