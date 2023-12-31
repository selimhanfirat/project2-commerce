# Generated by Django 4.2.4 on 2023-08-18 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='followers', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.ImageField(upload_to='listing_images'),
        ),
    ]
