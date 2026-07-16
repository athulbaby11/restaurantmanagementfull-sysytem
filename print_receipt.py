from escpos.printer import Usb, Network
from datetime import datetime

def print_receipt(order, printer_type='usb', usb_params=None, network_ip=None, paper_width=58):
    """
    Prints a restaurant receipt using ESC/POS thermal printer.

    Args:
        order (dict): {
            'restaurant_name': str,
            'items': [{'name': str, 'qty': int, 'price': float}],
            'subtotal': float,
            'grand_total': float
        }
        printer_type (str): 'usb' or 'network'
        usb_params (dict): {'idVendor': int, 'idProduct': int, ...}
        network_ip (str): Printer IP address for network printing
        paper_width (int): Paper width in mm (58 or 80)
    """
    char_width = 32 if paper_width == 58 else 48

    # Initialize printer
    if printer_type == 'usb':
        if not usb_params:
            raise ValueError("usb_params required for USB printer")
        p = Usb(**usb_params)
    elif printer_type == 'network':
        if not network_ip:
            raise ValueError("network_ip required for Network printer")
        p = Network(network_ip)
    else:
        raise ValueError("Invalid printer_type. Use 'usb' or 'network'.")

    # Header
    p.set(align='center', bold=True, height=2, width=2)
    p.text(order['restaurant_name'] + '\n')
    p.set(align='center', bold=False, height=1, width=1)
    p.text(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n')
    p.text('-' * char_width + '\n')
    # Table number and order placed by
    if 'table_number' in order:
        p.set(align='left')
        p.text(f"Table No: {order['table_number']}\n")
    if 'order_placed_by' in order:
        p.set(align='left')
        p.text(f"Order Placed By: {order['order_placed_by']}\n")
    p.text('-' * char_width + '\n')

    # Items
    p.set(align='left')
    p.text('{:<16}{:>5}{:>7}{:>7}\n'.format('Item', 'Qty', 'Price', 'Total'))
    p.text('-' * char_width + '\n')
    for item in order['items']:
        total = item['qty'] * item['price']
        name = item['name'][:16]
        qty = item['qty']
        price = item['price']
        p.text('{:<16}{:>5}{:>7.2f}{:>7.2f}\n'.format(name, qty, price, total))

    p.text('-' * char_width + '\n')
    p.text('{:<24}{:>7.2f}\n'.format('Subtotal:', order['subtotal']))
    if 'tax' in order:
        p.text('{:<24}{:>7.2f}\n'.format('Tax (20%):', order['tax']))
    elif 'vat' in order:
        p.text('{:<24}{:>7.2f}\n'.format('Tax (20%):', order['vat']))
    p.text('{:<24}{:>7.2f}\n'.format('Grand Total:', order['grand_total']))
    p.text('-' * char_width + '\n')

    # Footer
    p.set(align='center', bold=True)
    p.text('Thank You\n')
    p.text('Visit Again\n')
    p.cut()

# Example usage:
order_data = {
    'restaurant_name': 'Hotel Paradise',
    'items': [
        {'name': 'Fried Rice', 'qty': 2, 'price': 120.0},
        {'name': 'Paneer Curry', 'qty': 1, 'price': 150.0},
        {'name': 'Naan', 'qty': 3, 'price': 30.0}
    ],
    'subtotal': 480.0,
    'grand_total': 480.0
}
# For USB printer:
# print_receipt(order_data, printer_type='usb', usb_params={'idVendor': 0x04b8, 'idProduct': 0x0202}, paper_width=58)
# For Network printer:
# print_receipt(order_data, printer_type='network', network_ip='192.168.1.100', paper_width=80)
