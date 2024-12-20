# Generated by Django 5.1.1 on 2024-10-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0003_p_orders_delete_p_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='p_orders',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='pending', max_length=10),
        ),
    ]
