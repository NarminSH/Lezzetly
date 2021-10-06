
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cooks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='Title')),
                ('description', models.CharField(blank=True, max_length=255)),
                ('is_taste', models.BooleanField(default=False, verbose_name='Taste')),
                ('is_time', models.BooleanField(default=False, verbose_name='TimeOfDay')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stock_quantity', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('preparing_time', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ManyToManyField(blank=True, db_index=True, related_name='meals', to='meals.Category')),
                ('cook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='cooks.cook')),
                ('ingredients', models.ManyToManyField(blank=True, db_index=True, related_name='meals', to='meals.Ingredient')),
                ('mealoption', models.ManyToManyField(blank=True, db_index=True, related_name='meals', to='meals.MealOption')),
            ],
        ),
    ]
