# Generated by Django 4.0.3 on 2024-03-25 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_customer_id_order_product_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout_session_id',
            field=models.CharField(default=None, editable=False, max_length=200, null=True),
        ),
    ]