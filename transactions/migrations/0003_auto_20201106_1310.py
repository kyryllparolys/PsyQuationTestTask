# Generated by Django 3.1.3 on 2020-11-06 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20201105_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='account_id',
            new_name='account',
        ),
    ]
