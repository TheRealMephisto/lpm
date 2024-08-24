import { InformationElement } from './informationElement';

/**
 * // ToDo: Pending design decision
 * Either Base class, implementing core functionality handling the data from the backend,
 * which can be extended by other classes,
 * or similar the one model class just like in the backend.
 */
export class ContentObject {
    /**
     * information together with declaration of information type
     */
    protected optionalInformationArray: Array<InformationElement> = [];

    protected mandatoryInformationArray: Array<InformationElement> = [];

    protected Id: number;

    protected creationDate: Date = new Date();

    constructor(
        object: Object
    ) {
        if (!this.isValidObject(object)) {
            throw new Error("Invalid object");
        }

        this.Id = object["contentId"] ? object["contentId"] : -1;

        const mandatory_keys: Array<string> = object["mandatory_information"];

        const keys: Array<string> = Object.keys(object["available_information"]);
        
        for (const key of keys) {
            if (mandatory_keys.includes(key)) {
                this.mandatoryInformationArray.push(new InformationElement(key, object['available_information'][key]["DataType"], object['available_information'][key]["Value"], object['available_information'][key]["mandatory"], object['available_information'][key]["array"], object['available_information'][key]["Id"]));
            } else {
                this.optionalInformationArray.push(new InformationElement(key, object['available_information'][key]["DataType"], object['available_information'][key]["Value"], object['available_information'][key]["mandatory"], object['available_information'][key]["array"], object['available_information'][key]["Id"]));
            }
        }
    }

    private isValidObject(object: Object) {
	// ToDo: check if "optional_information_keys" was planned to be used
        // const needed_keys: Array<string> = ["optional_information_keys", "mandatory_information_keys", "available_information"];
        const needed_keys: Array<string> = ["mandatory_information", "available_information"];
        
        const keys = Object.keys(object);

        for (const key of needed_keys) {
            if (!keys.includes(key)) {
                return false;
            }
        }

        return true;
    }

    public getId(): number {
        return this.Id;
    }

    public getOptionalInformationArray(): Array<InformationElement> {
        return this.optionalInformationArray;
    }

    public getMandatoryInformationArray(): Array<InformationElement> {
        return this.mandatoryInformationArray;
    }

    public getDateString(): string {
        return this.creationDate.toDateString();
    }
}
