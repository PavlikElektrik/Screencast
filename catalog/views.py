# catalog/views.py
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, ContactInfo
from .forms import FeedbackForm, ProductForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .services import get_products_by_category
from .models import Category

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'page_obj'
    paginate_by = 6

    def get_queryset(self):
        return Product.objects.all()


class ContactsView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('contacts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = ContactInfo.objects.first()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Спасибо, {form.cleaned_data["name"]}! Ваше сообщение отправлено.')
        return super().form_valid(form)

@method_decorator(cache_page(60), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Автоматически привязываем текущего пользователя к продукту
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # Добавляем проверку
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        # Логика: Редактировать может только владелец
        product = self.get_object()
        return self.request.user == product.owner


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):  # Добавляем проверку
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        # Логика: Удалять может владелец ИЛИ пользователь с правом 'delete_product' (Модератор)
        product = self.get_object()
        user = self.request.user

        # Если пользователь владелец - разрешаем
        if user == product.owner:
            return True

        # Если у пользователя есть право удалять продукты - разрешаем
        if user.has_perm('catalog.delete_product'):
            return True

        return False

class CategoryListView(ListView):
    model = Product
    template_name = 'catalog/product_list_by_category.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Получаем category_id из URL
        category_id = self.kwargs.get('pk')
        # Используем нашу сервисную функцию с кешированием
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем название категории для заголовка
        category_id = self.kwargs.get('pk')
        context['category'] = Category.objects.get(pk=category_id)
        return context