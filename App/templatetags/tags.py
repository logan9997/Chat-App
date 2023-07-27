from django import template

register = template.Library()

@register.filter
def capitalise(string:str) -> str:
    return string.capitalize()


@register.filter()
def get(_dict:dict, key:str):
    return _dict.get(key)