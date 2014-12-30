def userschema():
    schema = {
        'name': {
            'type': 'dict',
            'schema': {
                'title':{
                  'type': 'string',
                  'minlength': 2,
                  'maxlength': 10,
                },
                'first': {
                    'type': 'string',
                    'minlength': 1,
                    'maxlength': 10,
                },
                'last': {
                    'type': 'string',
                    'minlength': 1,
                    'maxlength': 15,
                    'unique': True,
                },
            }
        },
        'email': {
            'type': 'string',
            'minlength': 1,
            'required': True,
            'unique': True,
        },
          'username': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 25,
            'unique': True,
        },
          'password': {
            'type': 'string'
        },
          'password_test': {
            'type': 'string'
        },
        'role': {
            'type': 'string',
            'default': 'normal',
            'allowed': ["admin", "normal", "test"],
        },
        'gender': {
            'type': 'string',
        },
        'location': {
            'type': 'dict',
            'schema': {
                'street': {'type': 'string'},
                'city': {'type': 'string'},
                'state': {'type': 'string'},
                'zip': {'type': 'string'}
            },
        },
        'picture': {
            'type': 'dict',
            'schema': {
                'large': {'type': 'string'},
                'medium': {'type': 'string'},
                'thumbnail': {'type': 'string'}
            },
        },
        'born': {
            'type': 'string',
        },
        'phone': {
            'type': 'string',
        },
        'friends':{
            'type': 'list',
            'schema': {
                'type':'objectid',
                'data_relation':{
                    'resource': 'userschema',
                    'embeddable': True
                }
            }
        }
    }
    user_schema = {
    # 'title' tag used in item links.
    'item_title': 'User',
    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform GET
    # requests at '/people/<lastname>/'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username'
    },

    'resource_methods': ['GET', 'POST', 'DELETE'],
    'item_methods': ['GET', 'PATCH', 'DELETE'],


    'public_methods': ['GET'],
    'public_item_methods': ['GET'],

    'schema': schema,

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.

    }
    return user_schema


def postschema():

    schema = {
        'author': {
            'type': 'objectid',
            'required': True
            },
        'type': {
            'type': 'string',
            'allowed': ["text", "image", "video"],
            },
        'content': {
            'type': 'string',
            'required': True
            },
        'location': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
                }
            }
        }

    post_schema = {
        'item_title': 'post',
        'url': 'postschema/<regex("[a-f0-9]{24}"):author>/posts',

        'resource_methods': ['GET', 'POST', 'DELETE'],
        'item_methods': ['GET', 'PATCH', 'DELETE'],

        'schema': schema
    }

    return post_schema
