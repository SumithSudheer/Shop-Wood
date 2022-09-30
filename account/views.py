import csv
import datetime
import random
# from product.views import product_home
import tempfile
from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect , HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from twilio.rest import Client
from django.contrib.auth.hashers import check_password
# from weasyprint import HTML
import product.views
from order.models import Payment, Order
from django.conf import settings
from .models import User, UserAddress

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter





# Create your views here.
num1 = 0
phone = 0

def index(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']





        print("-------------------------------------------------")
        try:
            user = authenticate(email=email, password=password )
        except:
            messages.error(request, ("user not found"))
        if user is not None:
            login(request, user)
            return redirect(product.views.product_home)
        else:
            messages.success(request, ("user not found"))


    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        try:
            password = request.POST['password']
            email = request.POST['email']
            phone = request.POST['phonenumber']
            name = request.POST['name']
            print(email)
            print(password)

            try:
                user = User.objects.create_user(email=email, password=password, phone=phone, name=name)
                print("done")
                return redirect(login)
            except :

                if User.objects.get(email=email) is not None:
                    messages.error(request, ("email already exist"))

                elif User.objects.get(phone=phone) is not None:
                    messages.error(request, ("phone already exist"))
                else:
                    messages.error(request, ("Enter Valid Details"))

        except :
            messages.error(request, ("Enter Valid Details"))

    return render(request, 'signup.html')


def otp(request):
    global num1
    global phone
    # if request.user.is_authenticated:
    #     return redirect(home)

    if request.method == 'POST':
        phone = request.POST['phone']
        num1 = random.randint(1000, 9999)
        print(num1)
        # account_sid = 'AC453029dd9c26c3bd962b94dc106f345d'
        # auth_token = '5cc6bb93f16bdef183a1282f872addd0'
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
    # if request.user.is_authenticated:
    #     return redirect(home)
    if request.method == 'POST':
        print("hlolololololo")
        otp = request.POST['otp']
        user = User.objects.get(phone=phone)
        print(otp)
        print(type(otp))
        print(num1)
        print(type(num1))
        print(user)

        if int(num1) == int(otp):
            print("1")

            login(request, user)
            return redirect(product.views.product_home)
    return render(request, 'otpconfirm.html')

# def home(request):
#     if request.user.is_authenticated:
#         return render(request, 'home-v1.html')

def account_view(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    return redirect(index)

def change_pass(request):
    if request.user.is_authenticated:
        print("--------------------------")

        if request.method == 'POST':
            password = request.POST['password']
            newpassword = request.POST['newpassword']
            confirmpassword = request.POST['confirmpassword']

            p = check_password(password, request.user.password)
            print(p)
            if newpassword == confirmpassword:
                if p:
                    u = User.objects.get(id=request.user.id)
                    u.set_password(newpassword)
                    u.save()
        return render(request, 'Changepassword.html')
    return redirect(index)

def address_manage(request):
    if request.user.is_authenticated:
        ob = UserAddress.objects.filter(user = request.user)
        if request.method == 'POST':

            name = request.POST['name']
            phone = request.POST['phone']
            Email = request.POST['email']
            address1 = request.POST['address1']
            address2 = request.POST['address2']
            country = request.POST['country']
            state = request.POST['state']
            zip = request.POST['zip']
            add = UserAddress(user=request.user, name=name, phone=phone,email=Email, address1=address1, address2=address2, country=country, state=state, zip=zip)
            add.save()
        return render(request, 'address.html', context={'ob' : ob})
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
        UserAddress.objects.filter(id=id).update(user=request.user, name=name, phone=phone, email=Email, address1=address1, address2=address2,
                          country=country, state=state, zip=zip)

    return render(request, 'editaddress.html', context={'ob':ob})






def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(product.views.product_home)

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition']= 'attachment: filename=Expenses' + \
        str(datetime.datetime.now())+'.csv'
    writer = csv.writer(response)
    writer.writerow(['Payment_id','Payment_method','Amount_paid','created_at','user_id'])
    payment =  Payment.objects.all()
    a = []
    for i in product:
        o = Order.objects.filter(product_id=i.id).aggregate(Sum('total_price'))
        if o['total_price__sum'] is None or o is None:
            a.append({'title': i.title, 'price': 0})
        else:
            a.append({'title': i.title, 'price': o['total_price__sum']})

    for i in payment:
        writer.writerow([i.payment_id, i.payment_method, i.amount_paid, i.created_at, i.user_id  ])

    return response

def export_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0 )
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines =[]
    payment = Payment.objects.all()
    print(payment)
    for i in payment:
        lines.append(str(i.payment_id)+" | "+str(i.payment_method)+" | "+str(i.amount_paid)+" | "+str(i.created_at)+" | "+str(i.user.id ))


    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='pdf.pdf')



