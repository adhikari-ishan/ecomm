from django.shortcuts import render, redirect
from . models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.db.models import Q #helps to search for multiple data from db
import json
from cart.cart import Cart
# Create your views here.


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        #db query model and icontains helps to search for products without case sensative
        searched = Product.objects.filter(Q(name__icontains = searched) | Q(description__icontains = searched))
        #for null search
        if not searched:
            messages.success(request,"Product is not available right now please try again later")
            return render(request,"search.html", { })
        else:
            return render(request,"search.html", { 'searched': searched })
    else:
        return render(request,"search.html", {  })


def update_info(request):
    if request.user.is_authenticated:
        #get ciuurent user info
        current_user = Profile.objects.get(user__id=request.user.id)
        # current_user, created = Profile.objects.get_or_create(user=request.user)
        #get shipping user info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        #get user form 
        form = UserInfoForm(request.POST or None, instance=current_user)
        #get shipping form 
        shipping_form = ShippingForm(request.POST or None,instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request,"your info has been updated!!!")
            return redirect('home')
        return render(request,"update_info.html", { 'form':form, 'shipping_form':shipping_form })
    else:
        messages.success(request,"Log in to access the page!!")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Your Password has been updated ")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request,"update_password.html", { 'form': form })
    else:
        messages.success(request,"You must be logged in")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request,"User has been updated!!!")
            return redirect('home')
        return render(request,"update_user.html", { 'user_form':user_form })
    else:
        messages.success(request,"Log in to access the page!!")
        return redirect('home')


    #return render(request,'update_user.html', {})


def category_summary(request):
    categories = Category.objects.all()
    return render(request,'category_summary.html', {"categories": categories})


def category(request,foo):
    foo = foo.replace('-', ' ')  #replacing hyphens with spaces for url 
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'category.html', {'products':products, 'category' : category})

    except:
        messages.success(request, ("Category doesnot exists"))
        return redirect('home')



def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html', {'product':product})

def home(request):
    products = Product.objects.all()
    return render(request,'home.html', {'products':products})

def about(request):
    return render (request,"about.html",{})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            #for cart when logging in
            # current_user =  Profile.objects.get(id=request.user.id)
            current_user, created = Profile.objects.get_or_create(user=request.user)


            #gettting savef cart from database
            saved_cart = current_user.old_cart
            #converting db string into dictionary
            if saved_cart:
                #converting to dict using json
                converted_cart = json.loads(saved_cart)
                #gettting cart dict into session
                cart = Cart(request)
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)

            messages.success(request, ("Logged in Succesfully"))
            return redirect('home')
        else:
            messages.success(request, ("Error try again with right username and password"))
            return redirect('login')

    else:
        return render(request,'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("Logout successfully, thanks for using our product "))
    return redirect('home')
   
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #for login user 
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request,("User created, please update your profile"))
            return redirect('update_info')
        else:
               messages.success(request,("Error, please try again with correct credentials"))
               return redirect('register')
    else:    
        return render(request,'register.html',{'form':form})

