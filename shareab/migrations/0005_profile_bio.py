# Generated by Django 5.0 on 2024-06-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shareab', '0004_remove_profile_bio_alter_profile_social_media_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
