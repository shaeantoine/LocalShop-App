# Generated by Django 4.2.6 on 2023-10-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LocalShopApp", "0003_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
