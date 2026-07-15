CURRENCY_RATES = {
    'GBP': {'symbol': '£', 'rate': 1.0},
    'USD': {'symbol': '$', 'rate': 1.27},
    'EUR': {'symbol': '€', 'rate': 1.16},
    'INR': {'symbol': '₹', 'rate': 105.0},
    'JPY': {'symbol': '¥', 'rate': 188.0},
    'CNY': {'symbol': '¥', 'rate': 9.2},
    'AUD': {'symbol': 'A$', 'rate': 1.95},
    'CAD': {'symbol': 'C$', 'rate': 1.72},
    'CHF': {'symbol': 'CHF ', 'rate': 1.12},
    'SGD': {'symbol': 'S$', 'rate': 1.7},
    'NZD': {'symbol': 'NZ$', 'rate': 2.1},
    'HKD': {'symbol': 'HK$', 'rate': 9.9},
    'SEK': {'symbol': 'kr ', 'rate': 13.9},
    'NOK': {'symbol': 'kr ', 'rate': 13.7},
    'DKK': {'symbol': 'kr ', 'rate': 8.65},
    'PLN': {'symbol': 'zł ', 'rate': 5.7},
    'AED': {'symbol': 'د.إ ', 'rate': 4.65},
    'SAR': {'symbol': 'ر.س ', 'rate': 4.76},
}

CURRENCY_CHOICES = [
    ('GBP', 'British Pound (£)'),
    ('USD', 'US Dollar ($)'),
    ('EUR', 'Euro (€)'),
    ('INR', 'Indian Rupee (₹)'),
    ('JPY', 'Japanese Yen (¥)'),
    ('CNY', 'Chinese Yuan (¥)'),
    ('AUD', 'Australian Dollar (A$)'),
    ('CAD', 'Canadian Dollar (C$)'),
    ('CHF', 'Swiss Franc (CHF)'),
    ('SGD', 'Singapore Dollar (S$)'),
    ('NZD', 'New Zealand Dollar (NZ$)'),
    ('HKD', 'Hong Kong Dollar (HK$)'),
    ('SEK', 'Swedish Krona (kr)'),
    ('NOK', 'Norwegian Krone (kr)'),
    ('DKK', 'Danish Krone (kr)'),
    ('PLN', 'Polish Złoty (zł)'),
    ('AED', 'UAE Dirham (د.إ)'),
    ('SAR', 'Saudi Riyal (ر.س)'),
]

DEFAULT_CURRENCY = 'GBP'


def normalize_currency(code):
    code = (code or DEFAULT_CURRENCY).upper()
    if code not in CURRENCY_RATES:
        return DEFAULT_CURRENCY
    return code


def format_money(value, currency=DEFAULT_CURRENCY):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value

    currency = normalize_currency(currency)
    data = CURRENCY_RATES[currency]
    converted = amount * data['rate']
    return f"{data['symbol']}{converted:.2f}"
