# Generated by Django 3.2.7 on 2021-10-06 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cooks', '0001_initial'),
        ('meals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='cook',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='cooks.cook'),
        ),
        migrations.AddField(
            model_name='meal',
            name='ingredients',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='meals', to='meals.Ingredient'),
        ),
        migrations.AddField(
            model_name='meal',
            name='mealoption',
            field=models.ManyToManyField(blank=True, db_index=True, related_name='meals', to='meals.MealOption'),
        ),
    ]
