# Generated by Django 2.2.1 on 2019-06-15 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_auto_20190615_1532'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_bets',
            old_name='order',
            new_name='order_id',
        ),
        migrations.RenameField(
            model_name='order_path_info',
            old_name='order',
            new_name='order_id',
        ),
    ]
