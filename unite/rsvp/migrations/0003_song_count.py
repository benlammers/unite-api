# Generated by Django 3.1 on 2020-08-23 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rsvp', '0002_auto_20200823_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
