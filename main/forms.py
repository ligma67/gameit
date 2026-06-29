from django import forms
DESIGNS = {
    'input': "form-control block w-full rounded-md bg-white/5 px-3 py-1.5 text-base text-white outline-1 -outline-offset-1 outline-white/10 placeholder:text-gray-500 focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6",
    'file_upload':"cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 "
}
class reg_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':f"{DESIGNS['input']}", 'id':"exampleInputEmail1", "minlength":"4",'aria-describedby':"emailHelp"}) ,label='Имя пользователья', required=True, max_length=20)
    #email = forms.CharField(widget=forms.EmailInput(), label="Почта пользователья",required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':f"{DESIGNS['input']}", 'id':"exampleInputPassword1", 'placeholder':"Password"}), required=True)
    
class game_form(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': f"{DESIGNS['input']}", 'id':"game-name", "minlength":"4"}), label='Название игры', required=True, max_length=50)
    short_description = forms.CharField(widget=forms.Textarea(attrs={'class': f"{DESIGNS['input']}",'rows':'2', 'id':"game-short-description", "minlength":"5"}), label='Краткое описание игры', required=True, max_length=150)
    description = forms.CharField(widget=forms.Textarea(attrs={'class': f"{DESIGNS['input']}", 'rows':6, 'id':"game-description", "minlength":"15"}), label='Описание игры', required=True, max_length=500)
    game_icon = forms.ImageField(widget=forms.FileInput(attrs={'class':f"{DESIGNS['file_upload']}", "id":"gameIcon", "accept":"image/png, image/jpeg, image/svg, image/webp"}))
    game_link = forms.URLField(widget=forms.URLInput(attrs={'class':f"{DESIGNS['input']}", "id":"game-link", 'placeholder':"https://example.com"}), label="Ссылка на игру")