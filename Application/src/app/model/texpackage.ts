export class TeXPackage {
    name: string;
    options: Array<string>;

    constructor(name?: string, options?: Array<string>) {
        this.name = name;
        this.options = options;
    }
}