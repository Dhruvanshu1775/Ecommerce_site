# Generated by Django 3.1.2 on 2021-07-22 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20210722_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_price',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]