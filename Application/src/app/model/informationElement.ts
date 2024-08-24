export class InformationElement {
    public label: string;
    public dataType: string;
    public value: string;
    public mandatory: boolean;
    public array: boolean;
    public Id: number;

    constructor(label: string, dataType: string, value: string = '', mandatory: boolean = false, array: boolean = false, Id: number = undefined) {
        this.label = label;
        this.dataType = dataType;
        this.value = value;
        this.mandatory = mandatory;
        this.array = array;
        this.Id = Id;
    }
}