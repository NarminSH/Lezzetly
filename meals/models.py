from cooks.models import Cook
from django.db import models
from django.db.models.base import Model



class Category(Model):
    # relation
    parent = models.ManyToManyField('self', related_name='children', blank=True)

    # information
    title = models.CharField('Title', max_length=100, db_index=True)
    # image = models.ImageField('Şəkil', blank=True, upload_to='categories_images')
    description = models.CharField(max_length=255, blank=True)
    slug = models.SlugField('Slug', max_length=110, editable=False, default='', unique = True)
    is_main = models.BooleanField('Main', default=False)
    is_second = models.BooleanField('Second', default=False)
    is_third = models.BooleanField('Third', default=False)
    is_time = models.BooleanField('TimeOfDay', default=False)

    # moderations
    status = models.BooleanField('Aktiv', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('created_at', 'title')
        unique_together = ('slug',)
    

    @property
    def get_slug(self):
        slug = ''
        for item in self.parent.all():
            slug += item.title
        return slug


    def __str__(self):
        if self.is_main:
            title = f'{self.title}'
        elif self.is_second:
            title = f'{self.title}'
        else:
            title = f'{self.parent.all().last()} {self.title} '
        return title


# Create your models here.





class Meal(models.Model):
    #relations
    cook = models.ForeignKey(Cook, db_index=True, related_name='meals', on_delete=models.CASCADE)
    category = models.ManyToManyField('product.Category', related_name='categories')


    #information
    title = models.CharField(max_length=60)
    price = models.DecimalField(max_digits=5, decimal_places=2) 
    stock_quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    is_available = models.BooleanField()
    preparing_time = models.CharField(max_length=20)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_price(self):
        return self.price

    def __str__(self):
        return self.title


class Property(models.Model):
    #relation
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, db_index=True, related_name='properties')

    #information
    title = models.CharField(max_length=100)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PropertyOption(models.Model):
    #relation
    property = models.ForeignKey(Property, on_delete=models.CASCADE, db_index=True, related_name='options')

    #information
    title = models.CharField(max_length=100)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title




