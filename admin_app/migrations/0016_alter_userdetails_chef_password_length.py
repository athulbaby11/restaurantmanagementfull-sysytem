from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0015_subcategory_vat_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='chef',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
