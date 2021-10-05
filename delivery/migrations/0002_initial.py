# Generated by Django 3.2.7 on 2021-10-05 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('delivery', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryservice',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_services', to='orders.order'),
        ),
        migrations.AddField(
            model_name='deliveryarea',
            name='courier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_areas', to='delivery.courier'),
        ),
    ]
