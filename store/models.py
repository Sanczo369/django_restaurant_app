from django.db import models
from category.models import Category
from multiselectfield import MultiSelectField

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    ingredients     = models.TextField(max_length=500, blank=True)
    price           = models.DecimalField(max_digits=10, decimal_places=2)
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    
    ALLEGEN_CHOICES = [
        ('M', 'Mleko'),
        ('J', 'Jajka'),
        ('O', 'Orzechy'),
        ('S', 'Soja'),
        ('P', 'Pszenica'),
        ('Sk', 'Skorupiaki'),
    ]
    allergen = MultiSelectField(choices=ALLEGEN_CHOICES, blank=True, null=True, max_choices=6,
                                 max_length=6)
    
    
    def __str__(self):
        return self.product_name