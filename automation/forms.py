# from cProfile import label
# from attr import attrs
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class signupForm(UserCreationForm):
    password1= forms.CharField(
            widget=forms.PasswordInput
            (attrs={'class':'form-control',
            
                })
        )
    password2= forms.CharField(
            label='Confirm password (again)',
            widget=forms.PasswordInput
            (attrs={'class':'form-control',
            
                })
        )
    class Meta:
        model = User
        fields= ['username', 'email']
        labels= {'email': 'Email'}
        widgets= {
            'username' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
        }
class loginupForm(AuthenticationForm):
    password= forms.CharField(
            widget=forms.PasswordInput
            (attrs={'class':'form-control',
            
                })
        )
    username= forms.CharField(
            
            widget=forms.TextInput
            (attrs={'class':'form-control',
            
                })
        )


  