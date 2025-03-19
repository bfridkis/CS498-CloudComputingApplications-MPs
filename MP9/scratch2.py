{
    'Table': {
        'Name': 'string',
        'DatabaseName': 'string',
        'Description': 'string',
        'Owner': 'string',
        'CreateTime': datetime(2015, 1, 1),
        'UpdateTime': datetime(2015, 1, 1),
        'LastAccessTime': datetime(2015, 1, 1),
        'LastAnalyzedTime': datetime(2015, 1, 1),
        'Retention': 123,
        'StorageDescriptor': {
            'Columns': [
                {
                    'Name': 'string',
                    'Type': 'string',
                    'Comment': 'string',
                    'Parameters': {
                        'string': 'string'
                    }
                },
            ],
            'Location': 'string',
            'AdditionalLocations': [
                'string',
            ],
            'InputFormat': 'string',
            'OutputFormat': 'string',
            'Compressed': True|False,
            'NumberOfBuckets': 123,
            'SerdeInfo': {
                'Name': 'string',
                'SerializationLibrary': 'string',
                'Parameters': {
                    'string': 'string'
                }
            },
            'BucketColumns': [
                'string',
            ],
            'SortColumns': [
                {
                    'Column': 'string',
                    'SortOrder': 123
                },
            ],
            'Parameters': {
                'string': 'string'
            },
            'SkewedInfo': {
                'SkewedColumnNames': [
                    'string',
                ],
                'SkewedColumnValues': [
                    'string',
                ],
                'SkewedColumnValueLocationMaps': {
                    'string': 'string'
                }
            },
            'StoredAsSubDirectories': True|False,
            'SchemaReference': {
                'SchemaId': {
                    'SchemaArn': 'string',
                    'SchemaName': 'string',
                    'RegistryName': 'string'
                },
                'SchemaVersionId': 'string',
                'SchemaVersionNumber': 123
            }
        },
        'PartitionKeys': [
            {
                'Name': 'string',
                'Type': 'string',
                'Comment': 'string',
                'Parameters': {
                    'string': 'string'
                }
            },
        ],
        'ViewOriginalText': 'string',
        'ViewExpandedText': 'string',
        'TableType': 'string',
        'Parameters': {
            'string': 'string'
        },
        'CreatedBy': 'string',
        'IsRegisteredWithLakeFormation': True|False,
        'TargetTable': {
            'CatalogId': 'string',
            'DatabaseName': 'string',
            'Name': 'string',
            'Region': 'string'
        },
        'CatalogId': 'string',
        'VersionId': 'string',
        'FederatedTable': {
            'Identifier': 'string',
            'DatabaseIdentifier': 'string',
            'ConnectionName': 'string'
        },
        'ViewDefinition': {
            'IsProtected': True|False,
            'Definer': 'string',
            'SubObjects': [
                'string',
            ],
            'Representations': [
                {
                    'Dialect': 'REDSHIFT'|'ATHENA'|'SPARK',
                    'DialectVersion': 'string',
                    'ViewOriginalText': 'string',
                    'ViewExpandedText': 'string',
                    'ValidationConnection': 'string',
                    'IsStale': True|False
                },
            ]
        },
        'IsMultiDialectView': True|False,
        'Status': {
            'RequestedBy': 'string',
            'UpdatedBy': 'string',
            'RequestTime': datetime(2015, 1, 1),
            'UpdateTime': datetime(2015, 1, 1),
            'Action': 'UPDATE'|'CREATE',
            'State': 'QUEUED'|'IN_PROGRESS'|'SUCCESS'|'STOPPED'|'FAILED',
            'Error': {
                'ErrorCode': 'string',
                'ErrorMessage': 'string'
            },
            'Details': {
                'RequestedChange': {'... recursive ...'},
                'ViewValidations': [
                    {
                        'Dialect': 'REDSHIFT'|'ATHENA'|'SPARK',
                        'DialectVersion': 'string',
                        'ViewValidationText': 'string',
                        'UpdateTime': datetime(2015, 1, 1),
                        'State': 'QUEUED'|'IN_PROGRESS'|'SUCCESS'|'STOPPED'|'FAILED',
                        'Error': {
                            'ErrorCode': 'string',
                            'ErrorMessage': 'string'
                        }
                    },
                ]
            }
        }
    }
}