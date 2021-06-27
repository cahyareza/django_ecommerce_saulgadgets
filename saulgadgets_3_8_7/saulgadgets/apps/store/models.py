from django.db import models

# Create your models here.
# Create your models here.
class Category(models.Model):
    tittle = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ("ordering",)

    def __str__(self):
        return self.tittle

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null = True)
    price = models.FloatField()

    def __str__(self):
        return self.title