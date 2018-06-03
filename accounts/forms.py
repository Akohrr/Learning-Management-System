from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        exclude = ()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2

    def save(self, commit=True):
       user = super(UserCreationForm, self).save(commit = False) # Call the real save() method
       user.set_password(self.cleaned_data.get('password1'))
       if commit:
            user.save()

       return user