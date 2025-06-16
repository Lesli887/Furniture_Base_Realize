from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    # Добавляем поле для выбора способа оплаты
    PAYMENT_METHOD_CHOICES = [
        ('online', 'Оплата онлайн'),
        ('upon_receipt', 'Оплата при получении'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect,
        initial='online',
        label='Способ оплаты',
        required=True
    )

    class Meta:
        model = Order
        fields = ['address', 'phone', 'email', 'comment', 'payment_method']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'address': 'Адрес доставки *',
            'phone': 'Телефон *',
            'email': 'Email *',
            'comment': 'Комментарий к заказу',
        }