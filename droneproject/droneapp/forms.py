from django import forms
from .models import Restaurant

class RestaurantForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Create Your Password'}))
    menu_items = forms.MultipleChoiceField(
        choices=[
            ('Bakery', 'Bakery'),
            ('Coffee', 'Coffee'),
            ('Drink', 'Drink'),
            ('Food', 'Food'),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox h-5 w-5 text-blue-600'}),
        label="Menu Items"
    )

    class Meta:
        model = Restaurant
        fields = ['name', 'location', 'phone', 'email', 'password', 'menu_items', 'opening_time', 'closing_time', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Store name'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Store Address'}),
            'phone': forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'placeholder': 'Email'}),
            'opening_time': forms.TimeInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded', 'type': 'time'}),
            'icon': forms.FileInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded'}),
        }

