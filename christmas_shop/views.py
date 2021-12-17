from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product, Category
# Create your views here.
class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['title', 'hook_text', 'price', 'manufacturer', 'reserves', 'delivery_fee', 'image', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count()
        return context
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            return super(ProductCreate, self).form_valid(form)
        else:
            return redirect('/christmas_shop/')
class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'hook_text', 'price', 'manufacturer', 'reserves', 'delivery_fee', 'image', 'category']
    template_name = 'christmas_shop/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

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