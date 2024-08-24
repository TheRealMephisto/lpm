import { ContentObject } from "../model/content-object";
import { InformationElement } from "../model/informationElement";
import { TeXDocument } from "../model/texdocument";

export class ContentObjectHelper {

    public static createSceleton(type: string, specs: Array<InformationElement>): ContentObject {
        let mandatoryInformationArray: Array<string> = [];
        let availableInformation: Object = {};
        specs.map((spec: InformationElement) => {
          if (spec.mandatory) {
            mandatoryInformationArray.push(spec.label);
          }
          let value;
          switch (spec.dataType) {
            case "boolean":
              value = false;
              break;
            case "date":
              value = new Date();
              break;
            default:
              value = "";
          }
          availableInformation[spec.label] = {
            "DataType": spec.dataType,
            "Value": value
          };
        });
        let sceletonObject: Object = new Object({
            "mandatory_information": mandatoryInformationArray,
            "available_information": availableInformation
        });
        switch (type) {
            case "TexDocument":
              return new TeXDocument(sceletonObject);
            default:
              throw new Error("Can't create content object of unknown type!");
        }
      }
}
