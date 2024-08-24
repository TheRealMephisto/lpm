import { Component, OnInit, OnChanges, Input, SimpleChanges } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { TeXDocument } from '../model/texdocument';
import { DescriptiveItem } from '../model/descriptive-item';
import { ApiSpecs, BackendSpecs } from '../config/app-config';
import { InformationElement } from '../model/informationElement';

@Component({
  selector: 'app-detailview',
  templateUrl: './detailview.component.html',
  styleUrls: ['./detailview.component.scss']
})
export class DetailviewComponent implements OnInit, OnChanges {

  @Input() selectedDocument: TeXDocument;

  public descriptedDetails: Array<DescriptiveItem>;

  public packagesTree: Object;

  documentForm = new FormGroup({
    title: new FormControl(''),
    packages: new FormControl(''),
    keywords: new FormControl(''),
  })

  constructor() { }

  ngOnInit() {
  }

  ngOnChanges(change: SimpleChanges) {
    this.setDescriptedDetails();
  }

  compile() {
    console.info("This feature is work in progress");
    // console.log(this.selectedDocument);
  }

  // ToDo: finish implementation
  /** The development of this function has not been finished! */
  public getPdfURI(): string {
    let uri = "";
    let relFilePath: string = this.selectedDocument.getRelativePdfPath();

    if (relFilePath) {
      // uri = BackendSpecs.uri + relFilePath;
      return "/assets" + relFilePath;
    }

    return "/assets/NoPreviewAvailable.pdf"

    return uri;
  }

  public hasPdf(): boolean {
    return !!(this.getPdfURI());
  }

  public getTexFileURI(): string {
    return BackendSpecs.uri + BackendSpecs.texFilesFolder + this.selectedDocument.mainFilePath;

  }

  public setDescriptedDetails() {
    let arrayLabels: Array<string> = [];
    let arrayDetails: Array<Array<DescriptiveItem>> = [];
    this.descriptedDetails = this.selectedDocument.getMandatoryInformationArray().map(info => {
      if (info["label"] == "Dateipfad") {
        return new DescriptiveItem("Dateipfad", info.value);
      }
    })
    .concat(
      this.selectedDocument.getOptionalInformationArray().map(info => {
          return new DescriptiveItem(info.label, info.value);
      })).filter(descriptiveElement => {
        return descriptiveElement != undefined;
      }).concat(arrayLabels.map(label => {
        return new DescriptiveItem(label, arrayDetails[label], true);
      })
    );
  }
}
