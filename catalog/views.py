# catalog/views.py
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product, ContactInfo
from .forms import FeedbackForm

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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'