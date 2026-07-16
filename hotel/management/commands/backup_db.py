from datetime import datetime
from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a timestamped backup of db.sqlite3 and clean old backups."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            default="backups",
            help="Directory (relative to BASE_DIR or absolute) where backups are stored.",
        )
        parser.add_argument(
            "--keep",
            type=int,
            default=60,
            help="How many latest backup files to keep.",
        )

    def handle(self, *args, **options):
        db_path = Path(settings.BASE_DIR) / "db.sqlite3"
        if not db_path.exists():
            raise CommandError(f"Database file not found: {db_path}")

        output_dir = Path(options["output_dir"])
        if not output_dir.is_absolute():
            output_dir = Path(settings.BASE_DIR) / output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = output_dir / f"db_backup_{timestamp}.sqlite3"
        shutil.copy2(db_path, backup_file)

        keep = max(1, options["keep"])
        backups = sorted(output_dir.glob("db_backup_*.sqlite3"), key=lambda p: p.stat().st_mtime, reverse=True)
        for old_file in backups[keep:]:
            old_file.unlink(missing_ok=True)

        self.stdout.write(self.style.SUCCESS(f"Backup created: {backup_file}"))
