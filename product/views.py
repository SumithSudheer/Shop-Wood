# # from decimal import Decimal
#
import random
from datetime import datetime

from django.utils import timezone
import json

from django.shortcuts import render, redirect
#
# import account.views
from django.utils.datastructures import MultiValueDictKeyError

from account.models import UserAddress
from order.views import homepage
from product.models import Product ,Category, Coupons
from .models import CartItem
from account.views import index
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from order.models import Order, Billing_address, Payment
from order import views
from django.shortcuts import render
import razorpay
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse


#
# # Create your views here.
#
def product_home(request):
    products = Product.objects.all().values('title', 'description', 'price', 'inventory', 'image1', 'id')[0:3]
    products1 = Product.objects.all().values('title', 'description', 'price', 'inventory', 'image1', 'id')[0:6]
    print(products1)
    return render(request, 'home-v1.html', context={'products' : products, 'products1' : products1})

def productview(request,id):
    product_test=Product.objects.all()[:3]
    products = Product.objects.get(id=id)
    print("----------------------------------------------------------")
    print(product_test)
    offr_price = (products.price - (products.price * products.category.offer)/100)
    print(offr_price)
    if request.method=='POST' and request.user.is_authenticated:
        cid = request.POST['cid']
        cart_temp = CartItem.objects.filter(product=cid, user=request.user.id)
        if not cart_temp:
            quantity = request.POST['commerce-add-to-cart-quantity-input']
            print("ivdeyumm ethunund")
            product = Product.objects.get(id=cid)
            cat_itm = CartItem(product=product, unit_price=product.price,quantity=quantity, total_price=product.price * int(quantity),
                               user_id=request.user.id)
            cat_itm.save()
        else:
            quantity = request.POST['commerce-add-to-cart-quantity-input']
            product = Product.objects.get(id=id)
            cart_temp = CartItem.objects.get(product=cid, user=request.user.id)
            print(cart_temp)
            CartItem.objects.filter(product=id, user=request.user.id).update(quantity=int(quantity)+int(cart_temp.quantity), total_price =product.price*(int(quantity)+int(cart_temp.quantity)))
    product_list=[]
    for i in product_test:
        product_list.append({'title':i.title, 'description':i.description, 'image1':i.image1, 'price':i.price, 'offer_price':(i.price - (i.price * i.category.offer)/100)})

    id1 = int(id)
    product_view = request.path
    print(request.path)
    print(product_view)
    if request.path == str(product_view):
        print("hello")
    return render(request, 'productview.html', context={'products' : products, 'offr_price' : offr_price, 'id1':id1, 'product_view':product_view,'product_list':product_list } )



@csrf_exempt
def products(request):
    category = Category.objects.values('name', 'id').order_by('id')
    product1 = Product.objects.values('id', 'title', 'description', 'price', 'inventory', 'image1')
    text = request.GET.get('search')

    if request.method == 'GET' and text is not None:
        product_view = request.path
        text=request.GET.get('search')
        print("--------------------------------------------------------------------")

        print(text)
        product = Product.objects.values('id','title', 'description', 'price', 'inventory', 'image1').annotate(search=SearchVector('title', 'description', 'price')).filter(search=text)
        table1 = Paginator(product, 6)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'collection-v1.html', context={'page_obj': page_obj, 'category' : category, 'product1' : product1,'product_view':product_view})
    print("bbbbbbbbb")
    product = Product.objects.values('id', 'title', 'description', 'price', 'inventory', 'image1')
    table1 = Paginator(product, 6)
    page_number = request.GET.get('page')
    page_obj = table1.get_page(page_number)
    product_view = request.path
    print(product_view)
    return render(request, 'collection-v1.html', context={'page_obj': page_obj, 'category': category, 'product1' : product1,'product_view':product_view})


#return  render(request, 'collection-v1.html', context={'product' : product, 'category' : category})

def productsf(request, id):
    category = Category.objects.values('id', 'name', 'id').order_by('id')
    print("aaaaaa")
    product1 = Product.objects.filter(category_id=id).values('id', 'title', 'description', 'price', 'inventory', 'image1')

    if request.GET.get('search') is not None:
        text = request.GET.get('search')
        print("--------------------------------------------------------------------")
        print(text)
        product = Product.objects.values('id', 'title', 'description', 'price', 'inventory', 'image1').annotate(
            search=SearchVector('id', 'title', 'description', 'price')).filter(search=text, category_id=id)
        table1 = Paginator(product, 6)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        product_view = request.path
        return render(request, 'collection-v1.html', context={'page_obj': page_obj, 'category': category,'id':id,'product_view':product_view})
    product = Product.objects.filter(category_id=id).values('id', 'title', 'description', 'price', 'inventory', 'image1')
    table1 = Paginator(product, 6)
    page_number = request.GET.get('page')
    page_obj = table1.get_page(page_number)
    product_view = request.path
    print(product_view)
    return  render(request, 'collection-v1.html', context={'product1' : product1,'page_obj' : page_obj, 'category' : category,'id':id,'product_view':product_view})

def addtocart(request,id):
    if request.user.is_authenticated:
        print("hello")
        print(id)
        quantity = 1

        product = Product.objects.get(id=id)
        print(product)
        # for i in product:
        #     print(i['price'])

        print(product.price)
        # print(type(product['title']))
        cat_itm = CartItem(product=product, unit_price=product.price, total_price=product.price*quantity, user_id=request.user.id)
        cat_itm.save()
        return redirect(viewCart)
        # cart = Cart(cart_item=cat_itm, user=request.user)
        # cart.save()
    else:
        return redirect(index)

def viewCart(request):
    if request.user.is_authenticated:
        cart = CartItem.objects.filter(user_id=request.user.id).order_by('-created_at')
        print(cart)
        k =[]
        for i in cart:
            k.append({'id':i.id, 'unit_price': i.unit_price, 'offer': (i.total_price-(i.product.category.offer*i.total_price)/100), 'quantity':i.quantity, 'total_price':i.total_price, 'product_title':i.product.title,'product_description':i.product.description, 'product_image':i.product.image1})

        for i in k:
            print(i)




        if request.method == 'POST':
            name = request.POST['Name']
            phone = request.POST['phone']
            email = request.POST['email']
            address = request.POST['address']
            address2 = request.POST['address2']
            country = request.POST['country']
            state = request.POST['state']
            zip = request.POST['zip']
            payment_method = request.POST['paymentMethod']
            for i in cart:
                order = Order(user = request.user, product=i.product_id, purchase_price=i.unit_price, quantity=i.quantity, total_price=i.total_price, payment_method="1" )
                order.save()
                Product.objects.filter(id=i.product_id).update(inventory=i.product_id.inventory-i.quantity)
                add = Billing_address(name=name, phone=phone, email=email, address=address, address2=address2, country=country, state=state, zip=zip, user = request.user, order=order)
                add.save()



        cart1 = []
        total_amount= 0
        # i=cart.product_id
        print("------------------------------")
        for i in k:
            total_amount += i['offer']
        print(total_amount)

        request.session['t'] = str(total_amount)
        print('--------------------------------')
        print(request.session['t'] )




        return render(request, 'Cart.html', context={'cart' : cart,'total_amount' :total_amount,'k':k })
    else:
        return redirect(index)

@never_cache
def iquantity_cart(request, id):
    cart = CartItem.objects.get(id=id)


    if cart.product.inventory > cart.quantity:
        q=cart.quantity+1
        CartItem.objects.filter(id=id).update(quantity=cart.quantity+1)
        cart = CartItem.objects.get(id=id)
        t=cart.unit_price*cart.quantity
        CartItem.objects.filter(id=id).update(total_price=cart.unit_price * cart.quantity)
    return redirect(viewCart)

@never_cache
def dquantity_cart(request, id):
    cart = CartItem.objects.get(id=id)
    if cart.quantity == 1:
        return remove_cart(request,id=id)

    if 0 < cart.quantity:
        q=cart.quantity-1

        CartItem.objects.filter(id=id).update(quantity=cart.quantity-1)
        cart = CartItem.objects.get(id=id)
        t = cart.unit_price * cart.quantity
        CartItem.objects.filter(id=id).update(total_price=cart.unit_price * cart.quantity)
    return redirect(viewCart)

def remove_cart(request, id):
    CartItem.objects.get(id = id).delete()
    return redirect(viewCart)


# t = 0

def check_out(request):

    s = None
    if request.user.is_authenticated:

        t = int(float(request.session['t']))
        cart = CartItem.objects.filter(user_id=request.user.id)
        ob = UserAddress.objects.filter(user=request.user)
        print(cart)
        k = []
        for i in cart:
            k.append({'id': i.id, 'unit_price': i.unit_price,
                      'offer': i.total_price - i.product.category.offer % i.total_price, 'quantity': i.quantity,
                      'total_price': i.total_price, 'product_title': i.product.title,
                      'product_description': i.product.description, 'product_image': i.product.image1})

        for i in k:
            print(i)

        cartid = []
        quantity = []
        for i in cart:
            cartid.append(i.product_id)
        print(cartid)

        # order id generator
        now = timezone.now()
        print(now)
        ord2 = str(datetime.now())+str(request.user.id)+str(random.randint(0,100))
        ord1 = ord2.translate({ord(':'): None,ord('-'): None, ord(' '): None, ord('.'): None})
        print("===================================")
        print(ord1)
        ordwer = Order.objects.filter(order_id=ord1)
        if ordwer is None:
            return redirect(check_out)
        # order id generator ends
        request.session['order_id_main'] = ord1
        # if request.method=='GET':
        #     print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        #     coupon = request.GET.get('code')
        #     print(coupon)

        if request.method == 'POST':

            if 'coupon' in request.POST:
                code = request.POST['code']
                print("code----------------------------------------------------------code1")
                print(code)
                try:
                    coup = Coupons.objects.get(coupon_code=code,coupon_start__lt=now, coupon_end__gt=now, coupon_min__lte=t )
                except Coupons.DoesNotExist:
                    return redirect(check_out)

                print(coup)
                s = t - ((t*coup.coupon_offer)/100)
                print(s)
                request.session['coupon_offer'] = coup.coupon_offer
                request.session['coupon_code'] = coup.coupon_code
                request.session['t'] = s

                return redirect(check_out)
            try:
                address = request.POST['address']
            except MultiValueDictKeyError:
                return HttpResponse('Select Address')

            payment_method = request.POST['paymentMethod']
            adds = UserAddress.objects.get(id=address)
            request.session['add'] = address
            request.session['cart'] = cartid
            print(adds)
            # global t

            # for i in cart:
            #     t+=i.total_price
            print(t)
            request.session['total'] = str(t)
            for i in cart:
                ins = Product.objects.all().get(id =i.product_id )
                request.session['coupon_code'] = None
                request.session['coupon_offer'] = None
                if ins.inventory > i.quantity:

                    order = Order(order_id=ord1, user = request.user, product= ins, purchase_price=i.unit_price, quantity=i.quantity, total_price=i.total_price, payment_method="1" )
                    print("save1")
                    order.save()
                    Product.objects.filter( id=i.product_id).update(inventory=ins.inventory - i.quantity)

                    add = Billing_address(order_id_Ref=ord1, name=adds.name, phone=adds.phone, email=adds.email, address1=adds.address1, address2=adds.address2, country=adds.country, state=adds.state, zip=adds.zip, user = request.user, order=order)
                    print("save2")
                    add.save()
                    CartItem.objects.filter(id=i.id).delete()
                else:
                    return redirect(check_out)
            k = int(t * 100)
            #Razor Pay
            if payment_method == 'RP':
                if request.method == 'POST':
                    amount = k
                    print(amount)
                    order_currency = 'INR'
                    client = razorpay.Client(
                        # auth=("rzp_test_Nf4iy5nJpLvtmt", "Y2D6cZPsAz452WAVT8VpDTM1")
                        auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET)
                    )
                    payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 0})
                    payment_id = payment['id']
                    request.session['payment']= payment
                    payment_status = payment['status']
                    print(payment)
                    if payment_status == 'created':

                        print(payment)
                        return render(request, "razor.html", {'payment': payment, 't' : t, "cart": cart,'RAZOR_KEY_ID':settings.RAZOR_KEY_ID})

                j = {'k': k}
                # return render(request, "razor.html", context={'j': j})
            if payment_method == 'PAYPAL':
                if request.method == 'POST':


                    print(t)
                    return render(request, "paypal.html", context={'t':t,'ord1':ord1, 'cart':cart})

            return redirect(products)

        return render(request, 'checkout.html', context={'ob' : ob, 'cart':cart, 't': t, 'k':k, 's':s } )


def razor_home(request):
    pass

@csrf_exempt
def success(request):
    response = request.POST
    add = request.session['add']
    adds = UserAddress.objects.filter(id=add)
    order_id_main = request.session['order_id_main']
    order_ins = Order.objects.filter(order_id=order_id_main)
    print(adds)
    cartid = request.session['cart']
    cart=[]
    for i in cartid:
        cart.append(Product.objects.all().get(id =i ))

    print(cart)

    total = request.session['total']
    print("=================================================")
    print(response)
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_signature' : response['razorpay_signature']
    }
    ins = Payment(user=request.user, payment_id=params_dict["razorpay_payment_id"], payment_method='razor', amount_paid=total,
                  status='Paid', order_id=order_id_main)
    ins.save()
    pay = Payment.objects.filter(order_id=order_id_main)

    client = razorpay.Client(auth=("rzp_test_Nf4iy5nJpLvtmt", "Y2D6cZPsAz452WAVT8VpDTM1"))
    try:
        client.utility.verify_payment_signature(params_dict)

        return render(request, 'success.html', context={'status': True, 'adds':adds, 'cart':cart ,'total':total, 'order_ins':order_ins, 'pay':pay})
    except:
        return render(request, 'success.html', context={'status':False})
    p = request.session['payment']
    print(p)
    return render(request, 'success.html')


@csrf_exempt
def successp(request):
    response = request.POST
    print(response)
    body = request.session['body']
    print(body)
    add = request.session['add']
    adds = UserAddress.objects.filter(id=add)

    cartid = request.session['cart']
    cart = []
    for i in cartid:
        cart.append(Product.objects.all().get(id=i))

    total = request.session['total']
    order_id_main = request.session['order_id_main']
    order_ins = Order.objects.filter(order_id=order_id_main)
    pay = Payment.objects.filter(order_id=order_id_main)

    return render(request, 'psuccess.html' ,context={'status': True, 'adds':adds, 'cart':cart ,'total':total, 'order_ins':order_ins, 'pay':pay})


def payments(request):

    body = json.loads(request.body)
    print (body)
    request.session['body']=body
    pay = Payment(user = request.user, payment_id= body['paypal_transaction_id'], payment_method='PayPal',amount_paid= request.session['total'],status='Paid', order_id = body['orderID'] )
    pay.save()

    data = {
        'order_number': body['orderID'],
        'transID': body['paypal_transaction_id'],
    }
    return JsonResponse(data)


def test(request):
    return render(request, 'paypal.html')

def user_order(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user_id=request.user.id).order_by('-id')
        table1 = Paginator(order, 5)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'order.html', context={'page_obj' : page_obj})
def order_cancel(request , id):
    order = Order.objects.get(id = id)
    if order.status and order.delivery_status == 'P':
        Order.objects.filter(id=id).update(status=False)

    return redirect(user_order)

def order_view(request, id):
    order_ins= Order.objects.filter(id=id)
    order= Order.objects.get(id=id)
    adds = Billing_address.objects.filter(order_id_Ref=order.order_id)
    return render(request, 'orderview.html', context={'order_ins' : order_ins, 'adds':adds})

def coupon_apply(request):
    print("llllllllllllllllllllllllllllllllllllllllllllllllllllllll")
    if request.user.is_authenticated:
        print("----------------------------------------------------------------------------")
        if request.method=='POST':
            print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
            coupon = request.POST.get['code']
            print(coupon)

        return redirect(check_out)

def coupon_remove(request):

    cart = CartItem.objects.filter(user_id=request.user.id).order_by('-created_at')
    print(cart)
    k =[]
    for i in cart:
        k.append({'id':i.id, 'unit_price': i.unit_price, 'offer': i.total_price-i.product.category.offer%i.total_price, 'quantity':i.quantity, 'total_price':i.total_price, 'product_title':i.product.title,'product_description':i.product.description, 'product_image':i.product.image1})
    total_amount = 0
    # i=cart.product_id
    print("------------------------------")
    for i in k:
        total_amount += i['offer']
    print(total_amount)

    request.session['t'] = str(total_amount)
    print('--------------------------------')
    print(request.session['t'])
    request.session['coupon_code'] = None
    request.session['coupon_offer'] = None
    return redirect(check_out)