from django import forms
from .models import Product
from django.core.exceptions import ValidationError

BANNED_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
    'бесплатно', 'обман', 'полиция', 'радар'
]


def validate_image(image):
    """Проверка размера (5Мб) и формата"""
    if image.size > 5 * 1024 * 1024:
        raise ValidationError("Файл больше 5 МБ!")
    if not image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError("Только .jpg или .png!")


class ProductForm(forms.ModelForm):
    image = forms.ImageField(validators=[validate_image], required=False, label="Изображение")

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            for word in BANNED_WORDS:
                if word in name.lower():
                    raise forms.ValidationError(f"Запрещенное слово: {word}")
        return name

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if desc:
            for word in BANNED_WORDS:
                if word in desc.lower():
                    raise forms.ValidationError(f"Запрещенное слово: {word}")
        return desc


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
