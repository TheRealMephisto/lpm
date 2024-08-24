import { TeXPackage } from './texpackage';
import { InformationElement } from './informationElement';
import { ContentObject } from './content-object';

export class TeXDocument extends ContentObject {

    public title: string;
    public mainFilePath: string;

    private dateString: string = "datehere"; // ToDo: implement proper type handling

    constructor(object: Object) {
        super(object);
        for (const info of this.mandatoryInformationArray) {
            if (info.label == "Titel") {
                this.title = info.value;
            } else if (info.label == "Dateipfad") {
                this.mainFilePath = info.value;
            }
        }
    }

    public getRelativePdfPath(): string {
        let info = this.optionalInformationArray.find(info => {
            if (info.label == "PdfVorschau") {
                return true;
            }
            return false;
        });
        if (!info) {
            return "";
        }
        return info.value;
    }

    public getId(): number {
        return this.Id;
    }
}
