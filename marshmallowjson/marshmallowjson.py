"""Main module."""
import collections
import itertools
import inspect
import json

from marshmallow import Schema, fields
from marshmallow import validate as mr_validate

mr_validators = {
    'containsonly': mr_validate.ContainsOnly,
    'email': mr_validate.Email,
    'equal': mr_validate.Equal,
    'length': mr_validate.Length,
    'noneof': mr_validate.NoneOf,
    'oneof': mr_validate.OneOf,
    'range': mr_validate.Range,
    'regexp': mr_validate.Regexp,
    'url': mr_validate.URL,
}

mr_fields = {
    'field': fields.Field,
    'raw': fields.Raw,
    'dict': fields.Dict,
    'list': fields.List,
    'string': fields.String,
    'uuid': fields.UUID,
    'number': fields.Number,
    'integer': fields.Integer,
    'decimal': fields.Decimal,
    'boolean': fields.Boolean,
    'float': fields.Float,
    'datetime': fields.DateTime,
    'time': fields.Time,
    'date': fields.Date,
    'url': fields.Url,
    'email': fields.Email,
    'nested': fields.Nested,
}


def get_function_args(function):
    """Obtain function args with arg-required info."""
    args = inspect.getfullargspec(function)
    args_with_defaults = dict(itertools.zip_longest(
        reversed(args.args or []),
        reversed(args.defaults or []),
        fillvalue='without_value'
    ))
    return [
        {
            "name": arg_name,
            "required": arg_value is 'without_value'
        }
        for arg_name, arg_value in args_with_defaults.items()
        if arg_name is not 'self'
    ]


def get_not_provided_args(real_args, suposed_args):
    """Obtain required args names that supposed_args must contains."""
    for arg in real_args:
        if arg.get('required') and arg.get('name') not in suposed_args.keys():
            yield arg.get('name')


def has_valid_args(args, function_name, functions):
    """Specify if exists sufficient args to a correct function call."""
    field_args = get_function_args(functions.get(function_name))
    not_provided_args = list(get_not_provided_args(field_args, args))
    if not_provided_args:
        fail_args(not_provided_args, function_name)


def fail_args(args, function):
    """Fail args."""
    raise(TypeError(
        "Args not found: {args} for {function} validator".format(
            args=args,
            function=function
        )
    ))


def fail_field(kind, field, name):
    """Fail field."""
    raise(TypeError(
        '{kind} is not a known kind in {name}.{field}'.format(
            kind=kind,
            field=field,
            name=name
        )
    ))


def fail_validator(kind, field, name):
    """Fail validator."""
    raise(TypeError(
        '{kind} is not a known validator kind in {name}.{field}'.format(
            kind=kind,
            field=field,
            name=name
        )
    ))


def validate(definition):
    """Validate a json definition schema."""
    types = json.load(definition, object_pairs_hook=collections.OrderedDict)
    known_fields = set(mr_fields.keys())
    for name, definition in types.items():
        for field, schema in definition.items():
            field_kind = schema.get('kind')
            if field_kind not in known_fields:
                fail_field(field_kind, field, name)

            if field_kind in mr_fields.keys():
                has_valid_args(schema, field_kind, mr_fields)

            if field_kind == 'list':
                items = schema.get('cls_or_instance')
                if items not in known_fields:
                    fail_field(items, field, name)

            validate = schema.get('validate')
            if validate:
                validator_kind = validate.get('kind')
                if validator_kind not in mr_validators.keys():
                    fail_validator(validator_kind, field, name)
                has_valid_args(validate, validator_kind, mr_validators)

        known_fields.add(name)
    return types


def build_field(name, schema):
    """Create field."""
    field_args = dict()
    field_args['required'] = schema.get('required', False)
    validate = schema.get('validate')
    if validate and validate.get('kind'):
        args = validate.copy()
        args.pop('kind', None)
        validator = mr_validators.get(validate.get('kind'))
        field_args['validate'] = validator(**args)

    args = schema.copy()
    args.pop('kind', None)
    args.pop('required', None)
    args.pop('validate', None)

    if args.get('cls_or_instance'):
        args['cls_or_instance'] = mr_fields.get(
            args.get('cls_or_instance')
        )

    field_args.update(args)
    field = mr_fields.get(schema.get('kind'))

    return field(**field_args)


def get_schema_from_dict(definition):
    """Build a schema from a json definition."""
    types = validate(definition)
    global_schema = dict()
    for name, definition in types.items():
        schemas = dict()
        global_schema[name] = dict()
        for field, schema in definition.items():
            if schema.get('kind') in mr_fields.keys():
                schemas[field] = build_field(field, schema)
                continue
            global_schema[name].update({
                field: mr_fields.get('nested')(
                    global_schema[field]
                )
            })
        global_schema[name].update(schemas)
        global_schema[name] = type(
            name, (Schema,), global_schema[name]
        )()

    return global_schema.get(name)
