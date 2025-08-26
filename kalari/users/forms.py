from django import forms
from .models import User
from django.core.exceptions import ValidationError
import re




class userRegister(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=20,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'id': 'confirm', 'name': 'confirm'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'address', 'image', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'username', 'name': 'username'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email','required':True}),
            'address': forms.TextInput(attrs={'id': 'address', 'name': 'address'}),
            'phone': forms.TextInput(attrs={'id': 'phone', 'name': 'phone','type' : "tel",'minlength' :10,'maxlength':10}),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'password': forms.PasswordInput(attrs={'id': 'pass', 'name': 'password'}),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'place': 'Place',
            'phone': 'Phone',
            'address': 'Address',
            'image': 'Image',
            'password': 'Password'
        }
        help_texts = {
            'username': ' '
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

    def clean_phone(self):
        phone = str(self.cleaned_data.get('phone'))

        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        
        if phone[0] not in ['6', '7', '8', '9']:
            raise ValidationError("Phone number must start with digits 6, 7, 8, or 9.")
        
        return phone

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required.")
       
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")

     
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")


        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")

 
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")

        return password



class tregister(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=20,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'id': 'confirm', 'name': 'confirm'})
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'address', 'image','bio','exp', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'name': 'name'}),
            'email': forms.EmailInput(attrs={'id': 'email', 'name': 'email','required':True}),
            'address': forms.TextInput(attrs={'id': 'address', 'name': 'address'}),
            'phone': forms.TextInput(attrs={'id': 'phone', 'name': 'phone','type' : "tel",'minlength' :10,'maxlength':10}),
            'image': forms.FileInput(attrs={'id': 'image', 'name': 'image'}),
            'bio':forms.Textarea(attrs={'id':'bio','name':'bio','placeholder':'Brief biography of instructor'}),
            'exp':forms.NumberInput(attrs={'id':'exp','name':'exp'}),
            'password': forms.PasswordInput(attrs={'id': 'pass', 'name': 'password'}),
      

        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'place': 'Place',
            'phone': 'Phone',
            'address': 'Address',
            'image': 'Image',
            'bio':'Bio',
            'exp':'Experience Years',
            'password': 'Password'
        }
        help_texts = {
            'name': ' '
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

    def clean_phone(self):
        phone = str(self.cleaned_data.get('phone'))

        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits.")
        
        if phone[0] not in ['6', '7', '8', '9']:
            raise ValidationError("Phone number must start with digits 6, 7, 8, or 9.")
        
        return phone

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required.")
       
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")

     
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")


        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")

 
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError("Password must contain at least one special character.")

        return password


