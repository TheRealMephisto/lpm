export class DescriptiveItem { // ToDo: can this be deprecated later thanks to InformationElement?
    public description: string;
    public value: string | Array<string>;
    public array: boolean;

    constructor(description: string, value: string, array: boolean = false) {
        this.description = description;
        this.value = value;
        this.array = array;
    }
}
