
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

def home(request):
    return render(request, 'home.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f'Спасибо, {name}! Ваше сообщение отправлено.')
        return redirect('contacts')
    return render(request, 'contacts.html')