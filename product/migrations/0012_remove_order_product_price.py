# Generated by Django 3.1.2 on 2021-07-22 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20210722_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_price',
        ),
    ]