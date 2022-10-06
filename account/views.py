import random
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from twilio.rest import Client
from django.contrib.auth.hashers import check_password
import product.views
from django.conf import settings
from .models import User, UserAddress
from product.models import Guest_Cart, CartItem

# num1 = 0
# phone = 0
# email = None


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
            if 'guest_key' in request.session:
                p = request.session['guest_key']
                guest_cart = Guest_Cart.objects.filter(user_ref=p)
                login(request, user)
                for i in guest_cart:
                    try:
                        cart = CartItem.objects.get(user=request.user, product=i.product)
                    except:
                        cart = None
                    if cart:
                        CartItem.objects.filter(user=request.user, product=i.product).update(quantity=cart.quantity+i.quantity)
                    else:
                        k = CartItem(user=request.user,product=i.product,quantity=i.quantity,total_price=i.total_price,unit_price=i.unit_price)
                        k.save()
                return redirect(product.views.product_home)
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


            name = request.POST['name']
            try:
                if not request.POST['phonenumber']:
                    user = User.objects.create_user(email=email, password=password, phone=None, name=name)
                else:
                    user = User.objects.create_user(email=email, password=password, phone=request.POST['phonenumber'], name=name)
                return redirect(index)
            except:
                if User.objects.get(email=email) is not None:
                    messages.error(request, ("email already exist"))
                elif User.objects.get(phone=request.POST['phonenumber']) is not None and request.POST['phonenumber'] is not None:
                    messages.error(request, ("phone already exist"))
                else:
                    messages.error(request, ("Enter Valid Details"))
        except:
            messages.error(request, ("Enter Valid Details"))
    return render(request, 'signup.html')


def otp(request):
    num1 = request.session['num1'] = 0
    request.session['phone'] = 0
    email = request.session['email'] = None
    if request.method == 'POST':
        phone = request.POST['phone']
        email = request.POST['email']
        num1 = random.randint(1000, 9999)
        request.session['num1'] = num1
        if 'emailbtn' in request.POST:
            request.session['email']=email
            try:
                user = User.objects.get(email=email)
            except:
                messages.error(request, ("Email Doesnt exist"))
                return redirect(otp)

            request.session['phone'] = 0
            send_mail(
                'OTP',
                'Your Otp For Login : ' + str(num1),
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

        else:
            try:
                client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
                message = client.messages.create(
                    body='otp : ' + str(num1),
                    from_='[+][1][5626627540]',
                    to='[+][91]' + str([phone])
                )
            except:
                messages.error(request, ("Something went Wrong"))
                return redirect(otp)
            email = None
        return redirect(otp_verify)
    return render(request, 'otp_login.html')


def otp_verify(request):
    num1 = request.session['num1']
    if request.method == 'POST':
        otp = request.POST['otp']
        if request.session['phone'] == 0:

            user = User.objects.get(email=request.session['email'])

        else:
            user = User.objects.get(phone=request.session['phone'])

        if int(num1) == int(otp):
            login(request, user)
            return redirect(product.views.product_home)
        else:
            messages.error(request, ("Wrong OTP"))

    return render(request, 'otpconfirm.html')


def account_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name1']
            phone = request.POST['phone']
            User.objects.filter(id=request.user.id).update(name=name)
            try:
                if request.POST['phone']:
                    User.objects.filter(id=request.user.id).update(phone=phone)
            except IntegrityError:
                messages.error(request, ("phone already exist"))
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

            if p:
                if newpassword == confirmpassword:
                    u = User.objects.get(id=request.user.id)
                    u.set_password(newpassword)
                    u.save()
                else:
                    messages.error(request, ("Password missmatch"))
            else:
                messages.error(request, ("Enter Valid Details"))

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
