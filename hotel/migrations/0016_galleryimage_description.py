# Migration for adding description field to GalleryImage
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0015_galleryimage_heroimage_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryimage',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
