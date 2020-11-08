# Generated by Django 3.1.3 on 2020-11-08 15:08

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_account__balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='opened_at',
            field=models.DateField(blank=True, default=django.utils.datetime_safe.date.today),
        ),
    ]
