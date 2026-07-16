from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0017_hash_existing_passwords'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='tax_percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
