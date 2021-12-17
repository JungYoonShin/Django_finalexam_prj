from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True) #동일한 이름의 카테고리 금지
    slug = models.SlugField(max_length=200, allow_unicode=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return f'/christmas_shop/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    price = models.IntegerField()
    manufacturer = models.CharField(max_length=30) #제조사
    reserves = models.IntegerField() #적립금
    delivery_fee = models.IntegerField() #배송비
    image = models.ImageField(upload_to='christmas_shop/images/%Y/%m/%d', blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    #author
    def __str__(self):
        return f'[{self.pk}]{self.title}'
    def get_absolute_url(self):
        return f'/christmas_shop/{self.pk}/'
