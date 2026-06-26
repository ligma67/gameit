from django import forms

class reg_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control", 'id':"exampleInputEmail1", 'aria-describedby':"emailHelp"}) ,label='Имя пользователья', required=True, max_length=20)
    #email = forms.CharField(widget=forms.EmailInput(), label="Почта пользователья",required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control", 'id':"exampleInputPassword1", 'placeholder':"Password"}), required=True)