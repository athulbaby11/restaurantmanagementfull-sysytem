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

## Database Backup (Every 8 Hours)

### Manual backup

Run this from project root:

```bash
python manage.py backup_db --output-dir backups --keep 90
```

- Backup files are created in `backups/`.
- Latest 90 backups are kept automatically.

### Automatic backup on Windows Task Scheduler

The project includes:

- `scripts/backup_db.ps1`
- A Windows wrapper batch file: `C:\Users\athul\run_hotel_backup.bat`

Wrapper content:

```powershell
python manage.py backup_db --output-dir backups --keep 90
```

Create task (run once in PowerShell):

```powershell
schtasks /Create /TN "Hotel DB Backup Every 8 Hours" /SC HOURLY /MO 8 /TR "C:\Users\athul\run_hotel_backup.bat" /F
```

Check task:

```powershell
schtasks /Query /TN "Hotel DB Backup Every 8 Hours" /V /FO LIST
```
