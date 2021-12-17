from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
# Create your views here.
class ProductList(ListView):
    model = Product
    ordering = '-pk'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count()
        return context

class ProductDetail(DetailView):
    model = Product
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    category = Category.objects.get(slug=slug)

    return render(request, 'christmas_shop/product_list.html',
                  {
                      'product_list': Product.objects.filter(category=category),
                      'categories': Category.objects.all(),
                      'no_category_post_count': Product.objects.filter(category=None).count(),
                      'category': category,
                  }
                  )