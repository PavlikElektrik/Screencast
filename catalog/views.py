from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Product, ContactInfo
from .forms import ProductForm
from django.core.paginator import Paginator


def home(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    latest_products = Product.objects.order_by('-created_at')[:5]
    for p in latest_products:
        print(f"Product: {p.name}, Created: {p.created_at}")

    context = {
        'page_obj': page_obj,

    }
    return render(request, 'home.html', context)


def contacts(request):
    contact_info = ContactInfo.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f'Спасибо, {name}! Ваше сообщение отправлено.')
        return redirect('contacts')
    return render(request, 'contacts.html', {'contact_info': contact_info})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
