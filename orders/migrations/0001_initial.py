# Generated by Django 3.2.7 on 2021-10-11 12:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('meals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('customer_last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('customer_phone', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '994709616969'. Up to 12 digits", regex='^994(?:50|51|55|70|77|99|10|60)[0-9]{7}$')])),
                ('customer_email', models.EmailField(max_length=254, verbose_name='email address')),
                ('complete', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_items', to='meals.meal')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
        ),
    ]
