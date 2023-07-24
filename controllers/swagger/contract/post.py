from config import Config

contract_post_schema = {
    'tags': {
        'contract'
    },
    'parameters': [{
        'name': 'contract data',
        'in': 'body',
        'required': True,
        'schema': {
            'id': 'ContractData',
            'type': 'object',
            'properties': {
                'contractType': {
                    'type': 'string',
                    'enum': ['artist', 'dealer']
                },
                'numAdditionalChairs': {
                    'type': 'integer',
                    'minimum': 0,
                    'maximum': Config().get_contract_limit('max_additional_chairs'),
                    'example': 2
                },
                'artistPhoneNumber': {
                    '$ref': '#/definitions/PhoneNumber'
                },
                'signerName': {
                    'type': 'string',
                    'example': 'Bob'
                },
                'signerEmail': {
                    'type': 'string',
                    'format': 'email'
                },
                'helpers': {
                    'type': 'array',
                    'maxItems': Config().get_contract_limit('max_helpers'),
                    'items': {
                        '$ref': '#/definitions/Helper'
                    }
                }
            },
            'required': [
                'contractType',
                'numAdditionalChairs',
                'artistPhoneNumber',
                'signerName',
                'signerEmail'
            ]
        }
    }],
    'definitions': {
        'Helper': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string'
                },
                'phoneNumber': {
                    '$ref': '#/definitions/PhoneNumber'
                }
            },
        },
        'PhoneNumber': {
            'type': 'integer',
            'minimum': 10000000000,
            'maximum': 99999999999,
            'example': 11234567890
        },
        'Error': {
            'type': 'object',
            'properties': {
                'error': {
                    'type': 'string',
                    'example': 'Error message'
                }
            },
            'required': [
                'error'
            ]
        }
    },
    'responses': {
        '200': {
            'description': 'Successfully created contract',
            'schema': {
                'type': 'object',
                'properties': {
                    'contractId': {
                        'type': 'integer'
                    },
                    'required': [
                        'contractId'
                    ]
                }
            }
        },
        '400': {
            'description': 'Failed to make contract',
            'schema': {
                '$ref': '#/definitions/Error'
            }
        },
        '404': {
            'description': 'Bad request',
            'schema': {
                '$ref': '#/definitions/Error'
            }
        },
        '500': {
            'description': 'Internal server error',
            'schema': {
                '$ref': '#/definitions/Error'
            }
        },
    }
}
