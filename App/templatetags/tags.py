from django import template
from datetime import datetime
from ..config import DATE_FORMAT

register = template.Library()

@register.filter
def capitalise(string:str) -> str:
    return string.capitalize()


@register.filter()
def get(_dict:dict, key:str):
    return _dict.get(key)

@register.filter()
def values(_dict:dict):
    return _dict.values()

@register.filter()
def items(_dict:dict):
    return _dict.items()

@register.filter
def date_format(date:datetime, format_string:str):
    return datetime.strptime(date, DATE_FORMAT).strftime(format_string)