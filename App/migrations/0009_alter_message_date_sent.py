# Generated by Django 4.2.3 on 2023-07-30 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_rename_datetime_sent_message_date_sent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date_sent',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]