// ToDo: design decision
// later maybe load everything needed from the api? (except the apiuri and the first call, of course)

class ApiDataKeys {
    public totalResultCount: string = 'totalResultCount';
    public totalTableContentCount: string = 'totalTableContentCount';
    public entries: string = 'entries';
    public packagesCount: string = 'packagesCount';
    public packages: string = 'packages';
    public package: string = 'package';
    public options: string = 'options';
    public optionsCount: string = 'optionsCount';
    public keywords: string = 'keywords';
    public keywordsCount: string = 'keywordsCount';
    public version: string = 'Version';
}

export class BackendSpecs {
    // ToDo: fill in from global configuration file / tool
    public static uri: string = "https://localhost";

    public static texFilesFolder: string = "/files/Tex/";
}

export class ApiSpecs {
    
    public static uri: string = BackendSpecs.uri + '/api';

    public static fileNotFoundPath: string = '/404.html';

    public static getInformationTypeMap: string = '/getInformationTypeMap';

    public static getTexDocumentSpecifications: string = '/getTexDocumentSpecifications';

    public static getContentObjectSpecifications: string = "/getContentObjectSpecification";

    public static getTexDocumentEntries: string = '/getTexDocumentEntries';

    public static addTexDocumentEntry: string = '/addTexDocumentEntry';

    public static addContentObject: string = "/addContentObject";

    public static editContentObject: string = '/editContentObject';

    public static editTexDocumentEntry: string = '/editTexDocumentEntry';

    public static dataKeys: ApiDataKeys = new ApiDataKeys();
}
