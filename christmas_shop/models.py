from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
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
    content = MarkdownxField()
    #author
    def __str__(self):
        return f'[{self.pk}]{self.title}'
    def get_absolute_url(self):
        return f'/christmas_shop/{self.pk}/'
    def get_content_markdown(self):
        return markdown(self.content)

class Comment(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE) #포스트 지우면 모든 댓글 지우기
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'
    def get_avatar_url(self):
        if self.author.socialaccount_set.exists():
            return self.author.socialaccount_set.first().get_avatar_url()
        else:
            return 'https://doitdjango.com/avatar/id/430/19268e6e03eef497/svg/{self.author.email}/'