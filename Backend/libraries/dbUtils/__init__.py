from configUtils import ConfigReader

with ConfigReader.ConfigReader() as configReader:
    config = configReader.get_db_config()['Database']

_basic_data_types = ['string', 'boolean', 'number', 'date']

_get_basic_tex_document_data_command = """SELECT JSON_OBJECT
            (
                'contentId', contents.id
            )
            FROM contents
            LIMIT %s, %s;"""

_get_filtered_tex_document_data_command = """SELECT JSON_OBJECT
            (
                'contentId', contents.id
            )
            FROM contents
            WHERE
                contents.id IN (%s"""

_get_available_tex_document_information_command = """SELECT
        JSON_OBJECT
        (
            'InformationType', specifications.label,
            'InformationContent', information.value,
            'DataType', specifications.dataType,
            'IsMandatory', specifications.mandatory,
            'IsArray', specifications.array,
            'Id', information.id
        )
            FROM
                contentRinformation
            INNER JOIN
                information
            ON
                contentRinformation.informationId = information.id
            INNER JOIN
                specifications
            ON
                information.specificationId = specifications.id
            WHERE
                contentRinformation.contentId = %s;"""

_get_available_tex_document_information_verbose_command = """SELECT
        JSON_OBJECT
        (
            'InformationType', specifications.label,
            'InformationContent', information.value,
            'DataType', specifications.dataType,
            'IsMandatory', specifications.mandatory
            'IsArray', specifications.array,
            'Id', information.id
        ),
        JSON_OBJECT
        (
            'contentId', contentRinformation.contentId,
            'id', contentRinformation.id,
            'informationId', contentRinformation.informationId
        )
        FROM
            contentRinformation
        INNER JOIN
            information
        ON
            contentRinformation.informationId = information.id
        INNER JOIN
            specifications
        ON
            information.specificationId = specifications.id
        WHERE
            contentRinformation.contentId = %s;"""

_get_filtered_content_ids_of_tex_documents_command = """SELECT DISTINCT
        contents.id
    FROM
        contents
    INNER JOIN
        contentRinformation
        ON
        contents.id = contentRinformation.contentId
    INNER JOIN
        information
        ON
        contentRinformation.informationId = information.id
    WHERE
        information.value LIKE %s
    ORDER BY contents.id;"""

_update_information_entry_command = """UPDATE
        information
    SET
        value = %s
    WHERE
        id = %s;
"""

_delete_content_entry_command = """DELETE
    FROM
        contents
    WHERE
        contents.id = %s;
    DELETE
    FROM
        contentRinformation
    WHERE
        contentRinformation.contentId = %s;
    DELETE
    FROM
        contentRuser
    WHERE
        contentRuser.contentId = %s;
"""

_unlink_information_from_content_entry_command = """DELETE
    FROM
        contentRinformation
    WHERE
        contentRinformation.contentId = %s
    AND
        contentRinformation.informationId IN (%s
"""