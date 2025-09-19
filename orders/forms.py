from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес доставки'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Почтовый индекс'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'address': 'Адрес',
            'postal_code': 'Почтовый индекс',
            'city': 'Город',
        }
