
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product,ContactInfo

def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for p in latest_products:
        print(f"Product: {p.name}, Created: {p.created_at}")
    return render(request, 'home.html', {'latest_products': latest_products})

def contacts(request):
    contact_info = ContactInfo.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f'Спасибо, {name}! Ваше сообщение отправлено.')
        return redirect('contacts')
    return render(request, 'contacts.html', {'contact_info': contact_info})