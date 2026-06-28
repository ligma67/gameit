from django import forms

class reg_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':"form-control block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6", 'id':"exampleInputEmail1", 'aria-describedby':"emailHelp"}) ,label='Имя пользователья', required=True, max_length=20)
    #email = forms.CharField(widget=forms.EmailInput(), label="Почта пользователья",required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6", 'id':"exampleInputPassword1", 'placeholder':"Password"}), required=True)