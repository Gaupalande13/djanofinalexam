# Generated by Django 5.0.3 on 2024-03-10 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp4", "0002_alter_product_discounted_price"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discounted_price",
            field=models.IntegerField(),
        ),
    ]
