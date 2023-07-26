from config import Config

contract_post_schema = {
    'tags': [
        'contract'
    ],
    'parameters': [{
        'name': 'make contract',
        'in': 'body',
        'required': True,
        'schema': {
            'id': 'ContractData',
            'type': 'object',
            'properties': {
                'contractType': {
                    '$ref': '#/definitions/VendorType'
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
        'Roles': {
            'type': 'string',
            'enum': ['admin', 'reviewer']
        },
        'UUID': {
            'type': 'string',
            'example': '94953e00-4bfe-482c-813b-8f6454500380'
        },
        'VendorType': {
            'type': 'string',
            'enum': ['artist', 'dealer']
        },
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
            }
        },
        'UnauthorizedError': {
            'type': 'object',
            'properties': {
                'error': {
                    'type': 'string',
                    'example': 'Error message'
                },
                'description': {
                    'type': 'string',
                    'example': 'Request does not contain a well-formed access token in the \"Authorization\" header beginning with \"Bearer\"'
                }
            }
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
                    }
                }
            }
        },
        '400': {
            'description': 'Failed to make contract',
            'schema': {
                '$ref': '#/definitions/Error'
            }
        },
        '401': {
            'description': 'Unauthorized',
            'schema': {
                '$ref': '#/definitions/UnauthorizedError'
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
