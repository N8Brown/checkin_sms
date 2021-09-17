# Generated by Django 3.1.13 on 2021-09-17 17:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('text', '0010_auto_20210917_1313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userclient',
            old_name='last_received',
            new_name='last_message_received',
        ),
        migrations.RenameField(
            model_name='userclient',
            old_name='last_reply',
            new_name='last_message_reply',
        ),
        migrations.AddField(
            model_name='userclient',
            name='signed_up',
            field=models.DateField(blank=True, default=datetime.date(2021, 9, 17)),
        ),
    ]