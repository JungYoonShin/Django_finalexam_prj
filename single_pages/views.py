from django.shortcuts import render
from christmas_shop.models import Product
from christmas_shop.models import Product,Comment
# Create your views here.

def mypage(request):
    search = request.GET.get('search')
    writer = request.user
    replies = Comment.objects.filter(author=writer).order_by('-created_at')
    return render(request, 'single_pages/mypage.html', context={'replies': replies})
def about_company(request):
    return render(request, 'single_pages/about_company.html')
def landing(request):
    recent_products = Product.objects.order_by('-pk')[:3]
    return render(request, 'single_pages/landing.html', {'recent_products':recent_products})