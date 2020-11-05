# Generated by Django 3.1.3 on 2020-11-05 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('D', 'Debit'), ('C', 'Credit')], default=None, max_length=1),
            preserve_default=False,
        ),
    ]