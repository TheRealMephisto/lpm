import { TeXPackage } from './texpackage';

export class TeXDocument {

    /**
     * thema of the exercise, used as an identifier for the several version ofs the "same" exercise
     */
    public thema: string;
    /**
     * title of the exercise, might be different for different versions
     */
    public title: string;
    /**
     * Version of the exercise
     * 
     */
    public version: number;
    /**
     * Date of first creation
     */
    public creationDate: Date;
    /**
     * Keywords, which can be used to find the exercise
     */
    public keywords: Array<string>;
    /**
     * Packages and options needed to compile the exercise (LaTeX)
     */
    public packages: Array<TeXPackage>;
    /**
     * Path of the folder, containing .tex and needed files (like .jpg). Needs to contain a content_main.tex!
     */
    public rawDataPath: string;
    /**
     * Path of the output .pdf
     */
    public outputPath: string;
    
    constructor(
        thema: string = "",
        title: string = "",
        version: number = 0,
        creationDate: Date = new Date(),
        keywords: Array<string> = [""],
        packages: Array<TeXPackage> = [],
        rawDataPath: string = "",
        outputPath: string = ""
    ) {
        this.thema = thema;
        this.title = title;
        this.version = version;
        this.creationDate = creationDate;
        this.keywords = keywords;
        this.packages = packages;
        this.rawDataPath = rawDataPath;
        this.outputPath = outputPath;
    }

    /**
     * @returns The string formatted in german format
     */
    public getDateString(): string {
        return "".concat(this.creationDate.getDate().toString(),".",
                            this.creationDate.getMonth().toString(),".",
                            this.creationDate.getFullYear().toString());
    }

}
