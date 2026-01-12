from django import forms
from .models import Center,Director
from accounts.models import User
#--center form hadi xof il briti tzid xi haja 
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
#--add diractor form  hna--
from django import forms
from django.contrib.auth import get_user_model
from accounts.models import Director

User = get_user_model()

class DirectorCreationForm(forms.ModelForm):
    # Extra fields for User model
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'director@example.com'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••'})
    )
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name'})
    )
    
    class Meta:
        model = Director
        fields = ['qualification_cert', 'hired_at']
        widgets = {
            # Hna fin ghadi i-tla3 l-calendar (YYYY-MM-DD)
            'hired_at': forms.DateInput(attrs={'type': 'date'}),
            'qualification_cert': forms.TextInput(attrs={'placeholder': 'e.g. Master in Education'}),
        }

    # 1. Validation: Bach t-fada UNIQUE constraint error
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Had l-email déjà m-sajjel. Jarreb wahed akhor.")
        return email

    # 2. Save Logic: Creer User + Director
    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            full_name=self.cleaned_data['full_name'],
            role_type='director'
        )
        
        # Create the Director profile
        director = super().save(commit=False)
        director.user = user
        
        if commit:
            director.save()
        return director

class AssignDirectorForm(forms.ModelForm):
    # Definir l-field dyal director b queryset khawi fl-lowel
    director = forms.ModelChoiceField(
        queryset=Director.objects.none(),
        required=True,
        empty_label="Select a Director",
        widget=forms.Select(attrs={
            'class': 'premium-input w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all'
        })
    )

    class Meta:
        model = Center
        fields = ['director']

    def __init__(self, *args, **kwargs):
        # Nakhdo l-user li t-passa men l-view
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Hna n-filtrer l-directeurs:
        # 1. center__isnull=True: Bach may-banouch l-directeurs li khdamins deja f center akhor.
        # Note: Hit l-models dyalk ma-fihomch 'created_by', ghadi n-werriw ga3 l-directeurs li available.
        self.fields['director'].queryset = Director.objects.filter(center__isnull=True)
        
        # Ila derti labels khorin:
        self.fields['director'].label = "Available Directors"
    