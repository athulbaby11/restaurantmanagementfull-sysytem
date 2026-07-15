# Restaurant Management Full System

A Django-based restaurant management platform for menu browsing, team/table ordering, cart handling, reservations, billing, receipts, and revenue tracking.

## Features

- Menu browsing for guests and logged-in users
- Team/table-based waiter ordering flow
- User cart and checkout flow
- Reservation booking
- Order receipts and order history
- Admin, chef, team, and user role-based dashboards
- Currency selection support for admin reports and saved price views

## Tech Stack

- Django
- SQLite
- Bootstrap
- Pillow
- python-escpos

## Local Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. Start the development server:

```bash
python manage.py runserver
```

## Notes

- The project uses SQLite by default.
- Media files are stored under the `media/` folder.
- Currency selection is handled from the admin header.
