from django import template
from hotel.currency import DEFAULT_CURRENCY, format_money, normalize_currency

register = template.Library()


@register.filter
def money(value, currency='GBP'):
    return format_money(value, normalize_currency(currency or DEFAULT_CURRENCY))
