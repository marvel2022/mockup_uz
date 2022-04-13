from django.urls import reverse

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()
# from users.models import User
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    slug = models.SlugField(max_length=250, verbose_name="Slug")

    image = models.ImageField(upload_to="category-image/%d/%m/%Y/", blank=True, null=True, verbose_name="Image")
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name="Caption")

    active = models.BooleanField(default=False, verbose_name='Active Category')

    class Meta:
        ordering = ['name', ]
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    


class Tag(models.Model):
    # category = models.ManyToManyField(Category, verbose_name="Category")
    tag = models.CharField(max_length=50, verbose_name="Tag Name")

    def __str__(self):
        return self.tag


class UserViews(models.Model):
    mockup = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_views", verbose_name="Product")
    visitor_ip = models.GenericIPAddressField(default='0.0.0.0')

    def __str__(self):
        return f"{self.visitor_ip} on {self.mockup.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL, related_name='product_category', verbose_name="Category")

    file       = models.FileField(upload_to="mockup-file/%d/%m/%Y/", null=True, verbose_name="MockUp File")
    resolution = models.CharField(max_length=50, blank=True, null=True, verbose_name="Resolution")
    extension  = models.CharField(max_length=10, blank=True, null=True, verbose_name="Extension")

    name        = models.CharField(max_length=200, verbose_name="Name")
    slug        = models.SlugField(max_length=300, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    price       = models.FloatField(blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(100000000)), verbose_name="Price")
    discount    = models.FloatField(blank=True, null=True, validators=(MinValueValidator(0), MaxValueValidator(100000000)), verbose_name="Discount")
    paid        = models.BooleanField(default=True, verbose_name="Paid")
    free        = models.BooleanField(default=False, verbose_name="Free") 

    downloaded = models.SmallIntegerField(default=0)
    # viewed = models.SmallIntegerField(default=0)

    liked = models.ManyToManyField(User, blank=True, null=True, related_name="user_likes",)
    tags  = models.ManyToManyField(Tag, related_name="product_tags", verbose_name="Product Tags")

    published_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def __str_(self):
        return self.name + " | " + self.category.name

    def get_absolute_url(self):
        return reverse("core:detail", kwargs = {"slug": self.slug})
    
    @property
    def fileURL(self):
        try:
            url = self.file.url
        except:
            url=''
        return url
    
    @property
    def get_extension(self):
        import os
        name, extension = os.path.splitext(self.file.name)
        return extension

    @property
    def date(self):
        if self.published_at == self.updated_at:
            date = self.published_at
        else:
            date = self.updated_at
        return date

    @property
    def views_count(self):
        return UserViews.objects.filter(mockup=self).count()
    
    @property
    def total_like(self):
        return self.liked.count()


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image", verbose_name="Product")
    
    image = models.ImageField(upload_to="product-image/%d/%m/%Y/", verbose_name="Image")
    caption = models.CharField(max_length=300, blank=True, null=True, verbose_name="Caption")

    def __str__(self):
        return "image pk: "+str(self.pk)+self.product.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url        


class MockUp(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_file", verbose_name="Product")

    file = models.FileField(upload_to="mockup-file/%d/%m/%Y/", verbose_name="MockUp File")
    resolution = models.CharField(max_length=50, blank=True, null=True, verbose_name="Resolution")
    extension = models.CharField(max_length=10, blank=True, null=True, verbose_name="Extension")

    def __str__(self):
        return "File pk: "+str(self.pk)+self.product.name
    @property
    def fileURL(self):
        try:
            url = self.file.url
        except:
            url=''
        return url
    
    @property
    def get_extension(self):
        import os
        name, extension = os.path.splitext(self.file.name)
        return extension



