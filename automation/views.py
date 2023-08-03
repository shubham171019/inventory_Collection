# from email import message
from email import message
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
# Create your views here.

from .forms import signupForm, loginupForm


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginupForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.success(request, "Logged in Successfully !!")
                    return redirect('HomePageView')
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        form = loginupForm()
        return render(request = request, template_name="login_page.html", context={"form":form})
    else:
        return redirect('/automation/HomePageView/')

def user_logout(request):
    logout(request)
    return redirect('/login_up/')




# def login_page(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request=request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('HomePageView')
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.error(request, "Invalid username or password.")
#     form = AuthenticationForm()
#     return render(request = request, template_name="login_page1.html", context={"form":form})


################
# from django.shortcuts import render


def sign_up(request):
    if request.method == "POST":
        fm= signupForm(request.POST)
        if fm.is_valid():
            messages.success(request, 'Account created successfully !!!!')
            fm.save()
        else:
            messages.error(request, "Invalid Input Data")
    else:
        fm= signupForm()
    return render(request, 'sign_up.html',{'form': fm})




# from .forms import UserCreationForm

# def sign_up(request):
#     if request.method == "POST":
#         fm= UserCreationForm(request.POST)
#         if fm.is_valid():
#             messages.success(request, 'Account created successfully !!!!')
#             fm.save()
#         else:
#             messages.error(request, "Invalid Input Data")
#     else:
#         fm= UserCreationForm()
#     return render(request, 'sign_up1.html',{'form': fm})


