export class TeXPackage {
    name: string;
    options: Array<string>;

    constructor(name?: string, options?: Array<string>) {
        if (name) {
            this.name = name;
        }
        if (options) {
            this.options = options;
        }
    }
}