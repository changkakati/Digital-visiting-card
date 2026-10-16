from django import forms
from .models import VisitingCard

class VisitingCardForm(forms.ModelForm):
    class Meta:
        model = VisitingCard
        exclude = ['user', 'slug', 'qr_code']  # 👈 Exclude QR code field
