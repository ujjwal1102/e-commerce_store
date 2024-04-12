# Generated by Django 4.0.3 on 2024-03-10 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customer_city_customer_pin_code_and_more'),
        ('product', '0004_rename_product_image_id_productutils_product_id'),
        ('order', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.customer'),
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.DeleteModel(
            name='OrderDetail',
        ),
    ]