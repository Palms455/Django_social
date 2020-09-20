from django import forms

class LoginForm(forms.Form):
    # форма авторизации
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


