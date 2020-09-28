# Generated by Django 3.1 on 2020-09-25 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200925_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customizemodulename',
            name='customize_name',
            field=models.IntegerField(blank=True, choices=[(1, 'Contact'), (2, 'Product'), (3, 'Credit Note'), (4, 'Purhase Order'), (5, 'Invoice'), (6, 'Expense'), (7, 'Purchase Entry'), (8, 'Debit Note')], db_index=True, null=True),
        ),
        migrations.CreateModel(
            name='CustomizeDebitNoteView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debit_number', models.IntegerField(blank=True, choices=[(1, 'YES'), (0, 'NO')], db_index=True, default=0, null=True)),
                ('debit_reference', models.IntegerField(blank=True, choices=[(1, 'YES'), (0, 'NO')], db_index=True, default=0, null=True)),
                ('debit_vendor', models.IntegerField(blank=True, choices=[(1, 'YES'), (0, 'NO')], db_index=True, default=0, null=True)),
                ('debit_date', models.IntegerField(blank=True, choices=[(1, 'YES'), (0, 'NO')], db_index=True, default=0, null=True)),
                ('debit_total', models.IntegerField(blank=True, choices=[(1, 'YES'), (0, 'NO')], db_index=True, default=0, null=True)),
                ('customize_view_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.customizemodulename')),
            ],
        ),
    ]
