# Generated by Django 4.2.4 on 2023-08-19 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_category_listing_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='larger_image',
            field=models.ImageField(blank=True, null=True, upload_to='larger/listing_images'),
        ),
    ]
