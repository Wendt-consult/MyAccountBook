# Generated by Django 3.1 on 2020-09-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20200902_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicemodel',
            name='invoice_recurring_count',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoicemodel',
            name='invoice_recurring_repeat',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
