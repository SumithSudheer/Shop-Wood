
import random
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from twilio.rest import Client
from django.contrib.auth.hashers import check_password
import product.views
from django.conf import settings
from .models import User, UserAddress

num1 = 0
phone = 0


def index(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = authenticate(email=email, password=password)
        except:
            if User.objects.get(email=email) is None:
                messages.error(request, ("Wrong credential"))
            else:
                messages.error(request, ("User not found"))
        if user is not None:
            login(request, user)
            return redirect(product.views.product_home)
        else:
            try:
                user = User.objects.get(email=email)
            except:
                user = None
            if user is None:
                messages.error(request, ("user not found"))
            else:
                messages.success(request, ("Wrong credential"))
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        try:
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phonenumber']
            name = request.POST['name']
            try:
                user = User.objects.create_user(email=email, password=password, phone=phone, name=name)
                return redirect(login)
            except:
                if User.objects.get(email=email) is not None:
                    messages.error(request, ("email already exist"))

                elif User.objects.get(phone=phone) is not None:
                    messages.error(request, ("phone already exist"))
                else:
                    messages.error(request, ("Enter Valid Details"))
        except:
            messages.error(request, ("Enter Valid Details"))
    return render(request, 'signup.html')


def otp(request):
    global num1
    global phone
    if request.method == 'POST':
        phone = request.POST['phone']
        num1 = random.randint(1000, 9999)
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        message = client.messages.create(
            body='otp : ' + str(num1),
            from_='[+][1][5626627540]',
            to='[+][91]' + str([phone])
        )
        return redirect(otp_verify)
    return render(request, 'otp_login.html')


def otp_verify(request):
    global num1
    if request.method == 'POST':
        otp = request.POST['otp']
        user = User.objects.get(phone=phone)

        if int(num1) == int(otp):
            login(request, user)
            return redirect(product.views.product_home)
    return render(request, 'otpconfirm.html')


def account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name1']
            User.objects.filter(id=request.user.id).update(name=name)
            return redirect(account_view)
        return render(request, 'profile.html')
    return redirect(index)


def change_pass(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            password = request.POST['password']
            newpassword = request.POST['newpassword']
            confirmpassword = request.POST['confirmpassword']
            p = check_password(password, request.user.password)
            if newpassword == confirmpassword:
                if p:
                    u = User.objects.get(id=request.user.id)
                    u.set_password(newpassword)
                    u.save()
                else:
                    messages.error(request, ("Enter Valid Details"))
            else:
                messages.error(request, ("Password missmatch"))
        return render(request, 'Changepassword.html')
    return redirect(index)


def address_manage(request):
    if request.user.is_authenticated:
        ob = UserAddress.objects.filter(user=request.user)
        if request.method == 'POST':
            name = request.POST['name']
            phone = request.POST['phone']
            Email = request.POST['email']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            country = request.POST['country']
            state = request.POST['state']
            zip = request.POST['zip']
            add = UserAddress(user=request.user, name=name, phone=phone, email=Email, address1=address1,
                              address2=address2, country=country, state=state, zip=zip)
            add.save()
        return render(request, 'address.html', context={'ob': ob})
    return redirect(index)


def edit_address(request, id):
    ob = UserAddress.objects.filter(id=id)
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        Email = request.POST['email']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        country = request.POST['country']
        state = request.POST['state']
        zip = request.POST['zip']
        try:
            UserAddress.objects.filter(id=id).update(user=request.user, name=name, phone=phone, email=Email,
                                                 address1=address1, address2=address2,
                                                 country=country, state=state, zip=zip)
        except:
            pass
        return redirect(address_manage)
    return render(request, 'editaddress.html', context={'ob': ob})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(product.views.product_home)


