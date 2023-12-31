# Generated by Django 4.2.4 on 2023-08-18 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_user_watchlist_alter_listing_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='highest_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='listing',
            name='winning_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won', to='auctions.bid'),
        ),
    ]
