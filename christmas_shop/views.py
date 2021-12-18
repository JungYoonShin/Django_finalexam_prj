from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from .models import Product, Category
# Create your views here.
class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['title', 'hook_text', 'content', 'price', 'manufacturer', 'reserves', 'delivery_fee', 'image', 'category']

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
    fields = ['title', 'hook_text', 'content', 'price', 'manufacturer', 'reserves', 'delivery_fee', 'image', 'category']
    template_name = 'christmas_shop/product_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied



class ProductList(ListView):
    model = Product
    ordering = '-pk'
    paginate_by = 4
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductList, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

class ProductDetail(DetailView):
    model = Product
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Product.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
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
def new_comment(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(product.get_absolute_url())

    else:
        raise PermissionDenied