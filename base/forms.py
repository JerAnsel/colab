from django.forms import ModelForm
import django.forms as forms
from .models import Room, UploadImage, Profile
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserForm(ModelForm):
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'name': 'password2', 'class': 'form-control', 'id': "password2",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "Confirm Password"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'name': 'username', 'class': 'form-control', 'id': "Username",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "Username"}),
            'password': forms.PasswordInput(attrs={'name': 'password', 'class': 'form-control', 'id': "Password",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "Password"}),
            'password2': forms.PasswordInput(attrs={'name': 'password2', 'class': 'form-control', 'id': "password2",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "Password"}),
            'first_name': forms.TextInput(attrs={'name': 'first_name', 'class': 'form-control', 'id': "first_name",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "First Name", 'required':''}),
            'last_name': forms.TextInput(attrs={'name': 'lasst_name', 'class': 'form-control', 'id': "last_name",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "Last Name", 'required':''}),
            'email': forms.EmailInput(attrs={'name': 'email', 'class': 'form-control', 'id': "email",
            'aria-describedby': "inputGroupPrepend", 'placeholder': "Email", 'required':''})
        }
        

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "The passwords do not match."
            )    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'skills': forms.SelectMultiple(attrs={'multiple':''})
        }

class UserImage(ModelForm):  
    class Meta:  
        # To specify the model to be used to create form  
        model = UploadImage  
        # It includes all the fields of model  
        fields = '__all__'  

class RoomForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'id':"room_name_input", 'name':"name", 'class': 'form-control'}))
    
    topi = forms.Select(attrs={'id':"chest", 'name':"topic", 'class': 'form-control'})
    t = forms.CharField()
    class Meta:
        model = Room
        exclude = ['host', 'participants']