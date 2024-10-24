from django import forms
from .models import Service, Order, Review

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # We don't need any fields as we'll set them in the view

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
