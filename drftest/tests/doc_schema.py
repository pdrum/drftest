import json

from schema import And, Use, Schema


def is_json_serializable(data):
    if data is None:
        return True
    try:
        json.dumps(data)
        return True
    except Exception:
        return False


doc_schema = Schema({
    'method': And(Use(str)),
    'data': And(Use(is_json_serializable)),
    'url': And(Use(str)),
    'url_kwargs': And(Use(is_json_serializable)),
    'format': And(Use(str)),
    'headers': And(Use(is_json_serializable)),
    'success': And(Use(bool)),
    'meta': {
        'docs': And(Use(str)),
        'method_name': And(Use(str)),
        'class_name': And(Use(str)),
        'app_name': And(Use(str))
    },
    'response': {
        'data': And(Use(is_json_serializable)),
        'status': And(Use(int)),
    }
})
