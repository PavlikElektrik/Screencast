from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from .forms import UserRegisterForm
from .models import User

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        # Отправка письма
        send_mail(
            subject='Добро пожаловать!',
            message='Поздравляем с успешной регистрацией на нашей платформе!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return super().form_valid(form)