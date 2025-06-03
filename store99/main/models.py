from django.db import models

class Size(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class ClothingItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)

    available = models.BooleanField(default=True)

    sizes = models.ManyToManyField(Size, 
                                   through='ClothingItemSize',
                                   related_name='clothing_items',
                                   blank=True)
    
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE,
                                 related_name='clothing_items')
    
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    price = models.DecimalField(max_digits=20, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name
    
    def get_price_with_discount(self):
        return self.price * (100 - self.discount) / 100
    
class ClothingItemSize(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.size.name
    
    class Meta:
        unique_together = ('clothing_item', 'size')