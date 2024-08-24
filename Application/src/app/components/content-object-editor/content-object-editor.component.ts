import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { FormGroup, FormBuilder, FormArray, Validators } from '@angular/forms';
import { ContentObjectHelper } from 'src/app/helper/content-object-helper';
import { DataService } from '../../data.service';
import { ContentObject } from '../../model/content-object';
import { InformationElement } from '../../model/informationElement';

/**
 * Provide a form enabling the user to edit database entries, i.e. of TeX-Documents.
 */
@Component({
  selector: 'app-content-object-editor',
  templateUrl: './content-object-editor.component.html',
  styleUrls: ['./content-object-editor.component.scss']
})
export class ContentObjectEditorComponent implements OnInit {

  @Input() contentObject: ContentObject = undefined;

  @Input() contentObjectType: string;

  @Output() finished: EventEmitter<void> = new EventEmitter<void>();

  private isNewEntry: boolean = true;

  public isLoaded: boolean = false;

  public infoToAdd: Array<InformationElement> = [];

  public newInfo: InformationElement;

  public finishButtonsDisabled: boolean = false;

  public contentObjectForm: FormGroup = new FormGroup({
    mandatory: new FormArray([]),
    optional: new FormArray([])
  });

  constructor(
      private fb: FormBuilder,
      private dataService: DataService
    ) { }

  get mandatory(): FormArray {
    return this.contentObjectForm.get("mandatory") as FormArray;
  }

  get optional(): FormArray {
    return this.contentObjectForm.get("optional") as FormArray;
  }

  ngOnInit() {
    if (this.contentObject) {
      this.isNewEntry = false;
    }
    this.dataService.getContentObjectSpecifications(this.contentObjectType).subscribe((data: Array<InformationElement>) => {
      let _this = this;
      const sceleton = ContentObjectHelper.createSceleton(_this.contentObjectType, data);

      if (_this.isNewEntry) {
        _this.contentObject = sceleton;
      }

      for (const info of _this.contentObject.getMandatoryInformationArray()) {
        _this.mandatory.push(_this.fb.group({
            label: info.label,
            dataType: info.dataType,
            value: info.value,
            Id: info.Id,
            array: info.array
          },
          [Validators.required, Validators.minLength(1)]
        ));
      }
      for (const info of sceleton.getOptionalInformationArray()) {
        _this.infoToAdd.push(info);
      }
      _this.sortInfoToAdd()
      _this.newInfo = _this.infoToAdd[0];

      _this.isLoaded = true;
      if (!_this.isNewEntry) {
        _this.addExistingInformation();
      }
    });
  }
  
  public onSubmit(): void {
    this.finishButtonsDisabled = true;
    if (!this.isNewEntry) {
      this.dataService.editContentObject(this.contentObjectForm.value, this.contentObjectType, this.contentObject.getId()).subscribe(state => {
        if (state) {
          this.finishButtonsDisabled = false;
          this.finished.emit();
        } else {
	  // ToDo: change to language / translation strings
          console.warn("Es liegt ein Fehler im Eintrag vor!")
        }
      });
    } else {
      this.dataService.addNewContentObject(this.contentObjectForm.value, this.contentObjectType).subscribe(state => {
        if (state) {
          this.finishButtonsDisabled = false;
          this.finished.emit();
        } else {
	  // ToDo: change to language / translation strings
          console.warn("Es liegt ein Fehler im Eintrag vor!")
        }
      });
    }
  }

  public onAbort(): void {
    this.finished.emit();
  }

  public addExistingInformation(): void {
    let removeFromInfoToAdd: Array<InformationElement> = [];
    for (const info of this.contentObject.getOptionalInformationArray()) {
      this.optional.push(this.fb.group({
          label: info.label,
          dataType: info.dataType,
          value: info.value,
          Id: info.Id,
          array: info.array
        },
        [Validators.required, Validators.minLength(1)]
      ));
      if (!info.array) {
        removeFromInfoToAdd.push(info);
      }
    }
    this.reduceInfoToAddArray(removeFromInfoToAdd);
  }

  public addNewInformation(): void {
    this.optional.push(this.fb.group({
        label: this.newInfo.label,
        dataType: this.newInfo.dataType,
        value: "",
        array: this.newInfo.array,
        Id: this.newInfo.Id
      },
      [Validators.required, Validators.minLength(1)]
    ));
    this.reduceInfoToAddArray([this.newInfo]);
  }

  private reduceInfoToAddArray(infosToRemove: Array<InformationElement>) {
    this.infoToAdd = this.infoToAdd.filter((info: InformationElement) => {
      let index = infosToRemove.findIndex((infoToRemove: InformationElement) => {
        return info.label == infoToRemove.label;
      });
      return index == -1;
    });
    this.newInfo = this.infoToAdd[0];
  }

  private sortInfoToAdd(): void {
    this.infoToAdd.sort((a, b) => {
      let sortedLabels = [a["label"], b["label"]].sort();
      let index = sortedLabels.findIndex(label => {
        return a["label"] === label;
      });
      return index * 2 - 1;
    });
  }

  public removeInformation(index: number) {
    let removed_entry = this.optional.value[index];
    this.optional.removeAt(index);
    this.infoToAdd.push(new InformationElement(
        removed_entry["label"],
        removed_entry["dataType"],
        removed_entry["value"],
        false,
        removed_entry["array"],
        removed_entry["Id"]
      )
    );
    this.sortInfoToAdd();
  }
}
