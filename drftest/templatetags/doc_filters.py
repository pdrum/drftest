import json

from django import template
from django.utils.safestring import mark_safe

from drftest.uuid_encoder import UUIDEncoder

register = template.Library()


@register.filter
def to_json(value):
    return mark_safe(json.dumps(value, indent=4, sort_keys=True, cls=UUIDEncoder))
