export class Exercise {

    /**
     * title of the exercise
     */
    title: string;
    /**
     * Version of the exercise
     * 
     */
    version: number;
    /**
     * Date of first creation
     */
    creationDate: Date;
    /**
     * Keywords, which can be used to find the exercise
     */
    keywords: Array<string>;
    /**
     * Packages needed to compile the exercise (LaTeX)
     */
    packages: Array<string>;
    /**
     * Path of the folder, containing .tex and needed files (like .jpg). Needs to contain a content_main.tex!
     */
    rawDataPath: string;
    /**
     * Path of the output .pdf
     */
    outputPath: string;

}
