# Generated by Django 2.1.1 on 2018-10-27 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_auto_20181027_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='notification_id',
            field=models.CharField(max_length=100),
        ),
    ]
