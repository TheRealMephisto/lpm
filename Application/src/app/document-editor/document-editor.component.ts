import { Component, OnInit } from '@angular/core';
import { FormControl, Validators, FormGroup, FormBuilder } from '@angular/forms';

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

  constructor(private fb: FormBuilder) { }

  ngOnInit() {
    this.texdocumentForm.get('author').setValue('devUser');
  }

  public texdocumentForm = new FormGroup({
    title: new FormControl('', [Validators.required]),
    path: new FormControl('', [Validators.required, Validators.pattern('.*\.'.concat(this.fileEnding))]),
    author: new FormControl('', [Validators.required]),
    packages: this.fb.array([
      this.fb.group({
        package: new FormControl(''),
        options: this.fb.array([])
      })
    ])
  });

  getErrorMessage(target: string): string {
    let targetForm;
    switch(target) {
      case 'title':
        targetForm = this.texdocumentForm.get('author');
        break;
      case 'path':
        targetForm = this.texdocumentForm.get('author');
        break;
      case 'author':
        targetForm = this.texdocumentForm.get('author');
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

  public onSubmit() {
    console.log(this.texdocumentForm.value);
  }

}
