from django import forms 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from .models import Post

class signup_form(UserCreationForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':'Password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg','placeholder':'Confirm Password'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Username'}),help_text=None)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets = {'first_name':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'First Name'}),
                'last_name':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Last Name'}),
                'email':forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Email'})}

class login_form(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control form-control-lg','placeholder':'Username'}),required=True)
    password = forms.CharField(
        label= _("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control form-control-lg','placeholder':'Password'}),required=True
    )

class Add_post(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','desc']
        labels = {'title':'Title','desc':'Description'}
        widgets = {'title':forms.TextInput(attrs={'class':'postform form-control form-control-lg fw-bold fs-1 border-0','placeholder':'Title'}),
                'desc':forms.Textarea(attrs={'class':'textar postform form-control form-control-lg text-black fw-medium','rows':7,'placeholder':'Description'})}

