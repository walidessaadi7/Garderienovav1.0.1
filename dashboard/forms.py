from django import forms
from .models import Center

class CenterCreationForm(forms.ModelForm):
    class Meta:
        model = Center
        # Ghadi n-asta3mlo ghir 'name' 7it l-fields khorin ma-kayninsh f model Center
        fields = ['name'] 
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none transition-all',
                'placeholder': 'Smiyt l-center (masalan: Center El Amal)'
            }),
        }
        labels = {
            'name': 'center name',
        }