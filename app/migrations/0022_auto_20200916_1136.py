# Generated by Django 3.1 on 2020-09-16 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20200916_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_tax_details',
            name='opening_balance',
            field=models.CharField(blank=True, db_index=True, default=0.0, max_length=20, null=True),
        ),
    ]
