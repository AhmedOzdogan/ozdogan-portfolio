from django import forms
from .models import Messages, Reservations

class MessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'

class ReservationsForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['name', 'email', 'reservation_date', 'number_of_guests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com'
            }),
            'reservation_date': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'reservation_date',  #Flatpickr
                'placeholder': 'Select date and time'
            }),
            'number_of_guests': forms.NumberInput(attrs={
                'type': 'range',
                'class': 'form-range',
                'min': 1,
                'max': 10,
                'step': 1,
                'oninput': "this.nextElementSibling.value = this.value"
            }),
        }