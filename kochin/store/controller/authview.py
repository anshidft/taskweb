from django.shortcuts import render, redirect
from  django.contrib.auth import authenticate, login, logout
from django.contrib import messages 

from store.forms import CustomUserForm



def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registred Successfully! Continue to Login')
            return redirect('/login')

    context = {'form':form}
    return render(request,'store/auth/register.html',context )

def loginpage(request):
    # if the user is already sign in and he try to login again using url in search bar, he got alertify message like below 
    if request.user.is_authenticated:
        messages.warning(request, "You are Already Login!") 
        return redirect('/')
    else:

        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')

            user = authenticate(request, username=name, password=passwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in Successfully!")
                return redirect('/')
            else:
                messages.error(request, "Invalid Username or password")
                return redirect('/login')
    return render(request,'store/auth/login.html')

def logoutpage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged Out Successfully')
    return redirect('/')
