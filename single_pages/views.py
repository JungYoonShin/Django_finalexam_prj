from django.shortcuts import render

# Create your views here.
def mypage(request):
    return render(request, 'single_pages/mypage.html')
def about_company(request):
    return render(request, 'single_pages/about_company.html')
def landing(request):
    return render(request, 'single_pages/landing.html')