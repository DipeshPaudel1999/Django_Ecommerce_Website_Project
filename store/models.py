from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.


class ProductManager(models.Manager):
  ''''filtering out the all active products which are not out of stock and returning it in views of all_products'''
  def get_queryset(self):
    return super(ProductManager, self).get_queryset().filter(out_of_stock=False)

class Category(models.Model):
  name = models.CharField(max_length=255,db_index=True)
  slug = models.SlugField(max_length=255,unique=True)

  class Meta:
    verbose_name_plural='categories'

  def get_absolute_url(self):
      return reverse("store:category_list", args={self.slug})
  

  def __str__(self):
    return self.name


class Product(models.Model):
  category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
  title = models.CharField(max_length=255)
  author = models.CharField(max_length=255, default='Er. Dipesh')
  description = models.TextField(blank=True)
  image = models.ImageField(upload_to='images/', default='images/default.jpg')
  slug = models.SlugField(max_length=255)
  price = models.DecimalField(max_digits=4,decimal_places=2)
  in_stock = models.BooleanField(default=True)
  out_of_stock = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  objects = models.Manager()
  products = ProductManager()

  class Meta: 
    verbose_name_plural = 'Products'
    ordering = ('-created',)

  def get_absolute_url(self):
    return reverse('store:product_detail', args=[self.slug])

  def __str__(self):
    return self.title



