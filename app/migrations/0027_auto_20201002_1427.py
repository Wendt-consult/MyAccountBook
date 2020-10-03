# Generated by Django 3.1 on 2020-10-02 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20201002_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsmodel',
            name='product_category',
            field=models.IntegerField(blank=True, choices=[(1, 'Raw Material'), (2, 'Finished Goods'), (3, 'Consumable  & Stores” ')], db_index=True, default=0, null=True),
        ),
    ]
