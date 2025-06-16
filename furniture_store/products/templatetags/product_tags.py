from django import template
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag
def modify_query(**kwargs):
    """
    Создает строку запроса с обновленными параметрами
    """
    # Получаем текущие параметры запроса
    query = kwargs.pop('query', None) or {}

    # Обновляем параметры
    for key, value in kwargs.items():
        if value is not None:
            query[key] = value
        elif key in query:
            del query[key]

    return urlencode(query)