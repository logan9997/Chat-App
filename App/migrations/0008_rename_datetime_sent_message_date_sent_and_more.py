# Generated by Django 4.2.3 on 2023-07-30 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_message_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='datetime_sent',
            new_name='date_sent',
        ),
        migrations.AddField(
            model_name='message',
            name='time_sent',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
