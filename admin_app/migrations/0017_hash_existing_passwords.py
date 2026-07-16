from django.db import migrations
from django.contrib.auth.hashers import identify_hasher, make_password


def hash_plain_passwords(apps, schema_editor):
    userdetails = apps.get_model('admin_app', 'userdetails')
    chef = apps.get_model('admin_app', 'chef')

    for model in (userdetails, chef):
        for obj in model.objects.all().iterator():
            password = (obj.password or '').strip()
            if not password:
                continue
            try:
                identify_hasher(password)
            except Exception:
                obj.password = make_password(password)
                obj.save(update_fields=['password'])


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0016_alter_userdetails_chef_password_length'),
    ]

    operations = [
        migrations.RunPython(hash_plain_passwords, migrations.RunPython.noop),
    ]
