from django.db import models



class UseFullCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name='Category Name')
    slug = models.SlugField(max_length=300, verbose_name='Slug')

    class Meta:
        ordering = ['name', 'pk']
        verbose_name_plural = 'Category'
    
    def __str__(self):
        return self.name
    

class UseFull(models.Model):
    category = models.ForeignKey(UseFullCategory, null=True, on_delete=models.SET_NULL, related_name='usefull_category', verbose_name='Category')

    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Web Site Name')
    image = models.ImageField(upload_to='usefull-images/', blank=True, null=True, verbose_name='Site Logo')

    link = models.URLField(verbose_name='Site URL')

    free = models.BooleanField(default=False, verbose_name='Free')
    paid = models.BooleanField(default=False, verbose_name='Paid')

    class Meta:
        verbose_name_plural = 'Use Full'

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url