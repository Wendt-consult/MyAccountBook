# Generated by Django 3.1 on 2020-09-26 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20200926_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='unused_credit',
            field=models.CharField(blank=True, db_index=True, default='0.00', max_length=20, null=True),
        ),
    ]
