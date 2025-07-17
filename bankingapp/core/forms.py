from django import forms
from .models import User

class ClientForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave empty if you don't want to change it")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password) 

        if commit:
            user.save()

        return user