import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import User
from order.models import Order, Payment
from product.models import Category
from product.forms import *
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from django.db.models import Sum


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None and user.is_staff == True and user.active == True:
            login(request, user)
            return redirect(dashboard)
    return render(request, 'login_admin.html')


def dashboard(request):
    if request.user.is_authenticated and request.user.active:
        product = Product.objects.all()
        user_count = User.objects.all().count()
        order_price = Payment.objects.all().aggregate(Sum('amount_paid'))
        total_income = order_price['amount_paid__sum']
        order_count = Order.objects.all().count()
        product_count = product.count()
        a = []
        for i in product:
            o = Order.objects.filter(product_id=i.id).aggregate(Sum('total_price'))
            if o['total_price__sum'] is None or o is None:
                a.append({'title': i.title, 'price': 0})
            else:
                a.append({'title': i.title, 'price': o['total_price__sum']})
        return render(request, 'Dashboard.html',
                      context={'product': product, 'a': a, 'user_count': user_count, 'total_income': total_income,
                               'order_count': order_count, 'product_count': product_count})
    return redirect(index)


def usermanagement(request):
    if request.user.is_authenticated and request.user.active:
        text = request.GET.get('searchs')
        if text is not None:
            table = User.objects.annotate(search=SearchVector('id', 'name', 'email', 'phone')).filter(
                search=text).values('id', 'name', 'email', 'active', 'phone').order_by('id')
            table1 = Paginator(table, 10)
            page_number = request.GET.get('page')
            page_obj = table1.get_page(page_number)
            return render(request, 'usermanagement.html', context={'page_obj': page_obj})
        table = User.objects.all().values('id', 'name', 'email', 'active', 'phone').order_by('id')
        table1 = Paginator(table, 10)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'usermanagement.html', context={'page_obj': page_obj})
    return redirect(index)


def block_user(request, id):
    if request.user.is_authenticated and request.user.active:
        flag = User.objects.all().values('active').get(id=id)
        if flag['active'] == True:
            User.objects.filter(id=id).update(active=False)
            return redirect(usermanagement)
        else:
            User.objects.filter(id=id).update(active=True)
            return redirect(usermanagement)
    return redirect(index)


def categorymanagement(request):
    if request.user.is_authenticated and request.user.active:
        text = request.GET.get('searchs')
        if text is not None:
            table = Category.objects.annotate(search=SearchVector('id', 'name', 'offer')).filter(search=text).values(
                'id', 'name', 'offer').order_by('id')
            table1 = Paginator(table, 10)
            page_number = request.GET.get('page')
            page_obj = table1.get_page(page_number)
            return render(request, 'Categorymanagement.html', context={'page_obj': page_obj})
        table = Category.objects.all().values('id', 'name', 'offer').order_by('id')
        table1 = Paginator(table, 10)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'Categorymanagement.html', context={'page_obj': page_obj})
    return redirect(index)


def addcategory(request):
    if request.user.is_authenticated and request.user.active:
        if request.method == 'POST':
            name = request.POST['name']
            offer = request.POST['offer']
            ins = Category(name=name, offer=offer)
            ins.save()
        return render(request, 'addcategory.html')
    return redirect(index)


def editcategory(request, id):
    if request.user.is_authenticated and request.user.active:
        path = request.path
        if request.method == 'POST':
            name = request.POST['name']
            offer = request.POST['offer']
            Category.objects.filter(id=id).update(name=name, offer=offer)
        table1 = Category.objects.filter(id=id).values('name', 'offer')

        return render(request, 'editCategorymanagement.html', context={'table1': table1, 'path': path})
    return redirect(index)


def productmanagement(request):
    if request.user.is_authenticated and request.user.active:
        text = request.GET.get('searchs')
        if text is not None:
            table = Product.objects.annotate(search=SearchVector('id', 'title', 'category', 'price', 'inventory')
                                             ).filter(search=text).values('id', 'title', 'category', 'price',
                                                                          'inventory').order_by('id')
            table1 = Paginator(table, 10)
            page_number = request.GET.get('page')
            page_obj = table1.get_page(page_number)
            return render(request, 'productmanagement.html', context={'page_obj': page_obj})
        product = Product.objects.all().values('id', 'title', 'category', 'price', 'inventory').order_by('id')
        table1 = Paginator(product, 10)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'productmanagement.html', context={'page_obj': page_obj})
    return redirect(index)


@login_required(login_url='/manage/')
def addproduct(request):
    if request.user.is_authenticated and request.user.active:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()

            return render(request, 'addproduct.html', {'form': form})
        else:
            form = ProductForm()
            return render(request, 'addproduct.html', {'form': form})
    return redirect(index)


@login_required(login_url='/manage/')
def editproduct(request, id):
    if request.user.is_authenticated and request.user.active:
        product = Product.objects.get(id=id)
        path = request.path
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()

            return render(request, 'editproducts.html', context={'form': form, 'path': path})
        else:

            product = Product.objects.get(id=id)
            form = ProductForm(instance=product)

            return render(request, 'editproducts.html', context={'form': form, 'path': path})
    return redirect(index)


@login_required(login_url='/manage/')
def deleteproduct(request, id):
    if request.user.is_authenticated and request.user.active:
        Product.objects.filter(id=id).delete()
        return redirect(productmanagement)
    return redirect(index)


@login_required(login_url='/manage/')
def deletecategory(request, id):
    if request.user.is_authenticated and request.user.active:
        Category.objects.filter(id=id).delete()
        return redirect(categorymanagement)
    return redirect(index)


@login_required(login_url='/manage/')
def logout_user(request):
    if request.user.is_authenticated and request.user.active:
        logout(request)
        return redirect(index)

    return redirect(index)


def order_manage(request):
    if request.user.is_authenticated and request.user.active:
        text = request.GET.get('searchs')
        if text is not None:
            table = Order.objects.annotate(search=SearchVector('id', 'product_id', 'user_id', )
                                           ).filter(search=text).values('id', 'payment_method', 'payment_status',
                                                                        'delivery_status', 'product_id', 'user_id',
                                                                        'purchase_price', 'quantity', 'total_price',
                                                                        'status').order_by('id')
            table1 = Paginator(table, 1)
            page_number = request.GET.get('page')
            page_obj = table1.get_page(page_number)
            return render(request, 'orderManage.html.html', context={'page_obj': page_obj})
        order = Order.objects.all().order_by('id')

        table1 = Paginator(order, 1)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'orderManage.html', context={'page_obj': page_obj})
    return redirect(index)


def ordercancel(request, id):
    if request.user.is_authenticated and request.user.active:
        order = Order.objects.get(id=id)
        if order.status and order.delivery_status == 'P':
            Order.objects.filter(id=id).update(status=False)

        return redirect(order_manage)
    return redirect(index)


def delivery_status(request, id):
    ins = Order.objects.get(id=id)
    if ins.delivery_status == 'P':
        Order.objects.filter(id=id).update(delivery_status='S')
    elif ins.delivery_status == 'S':
        Order.objects.filter(id=id).update(delivery_status='D')
    return redirect(order_manage)


def coupon_management(request):
    if request.user.is_authenticated and request.user.staff and request.user.active:
        text = request.GET.get('searchs')
        if text is not None:
            table = Coupons.objects.annotate(search=SearchVector('coupon_name', 'coupon_code', 'coupon_offer', 'id')
                                             ).filter(search=text).values('id', 'coupon_name', 'coupon_code',
                                                                          'coupon_offer', 'coupon_min', 'coupon_start',
                                                                          ' coupon_end').order_by('id')
            table1 = Paginator(table, 1)
            page_number = request.GET.get('page')
            page_obj = table1.get_page(page_number)
            return render(request, 'orderManage.html.html', context={'page_obj': page_obj})
        order = Coupons.objects.all().order_by('id')

        table1 = Paginator(order, 1)
        page_number = request.GET.get('page')
        page_obj = table1.get_page(page_number)
        return render(request, 'cupounmanagement.html', context={'page_obj': page_obj})


def add_coupons(request):
    if request.user.is_authenticated and request.user.active:
        if request.method == 'POST':
            form = CouponForm(request.POST)

            if form.is_valid():
                form.save()

        form = CouponForm()
        return render(request, 'addcoupons.html', context={'form': form})
    return redirect(index)


def edit_coupons(request, id):
    if request.user.is_authenticated and request.user.active:
        coupons = Coupons.objects.get(id=id)
        if request.method == 'POST':
            form = CouponForm(request.POST, request.FILES, instance=coupons)

            if form.is_valid():
                form.save()

            return render(request, 'editcoupons.html', context={'form': form})
        else:

            coupons = Coupons.objects.get(id=id)
            form = CouponForm(instance=coupons)
            return render(request, 'editcoupons.html', context={'form': form})
    return redirect(index)


def sales_report(request):
    product = Product.objects.all()
    ymax = timezone.now()
    ymin = (timezone.now() - datetime.timedelta(days=365))
    yearly = Order.objects.filter(order_at__lte=ymax, order_at__gte=ymin)
    mmax = timezone.now()
    mmin = (timezone.now() - datetime.timedelta(days=30))
    monthly = Order.objects.filter(order_at__lte=mmax, order_at__gte=mmin)
    ymax = timezone.now()
    ymin = (timezone.now() - datetime.timedelta(days=7))
    weekly = Order.objects.filter(order_at__lte=ymax, order_at__gte=ymin)
    a = []
    n = 1
    subm = timezone.now()
    n = 4
    for i in range(4):
        k = 0
        for i in monthly:
            if i.order_at <= subm and i.order_at >= (subm - datetime.timedelta(days=7)):
                k += 1

        a.append({'name': 'week' + str(n), 'value': k})
        n -= 1
        subm = subm - datetime.timedelta(days=7)

    subw = timezone.now()
    n = 7
    b = []
    for i in range(7):
        k = 0
        for i in weekly:
            if i.order_at <= subw and i.order_at >= (subw - datetime.timedelta(days=1)):
                k += 1
        b.append({'name': 'day' + str(n), 'value': k})
        n -= 1
        subw = subw - datetime.timedelta(days=1)
    monthly_sales = list(reversed(a))
    weekly_sales = list(reversed(b))
    user_count = User.objects.all().count()
    order_price = Payment.objects.all().aggregate(Sum('amount_paid'))
    total_income = order_price['amount_paid__sum']
    order_count = Order.objects.all().count()
    product_count = product.count()
    payment = Payment.objects.all()
    return render(request, 'salesreport.html',
                  context={'monthly': monthly, 'yearly': yearly, 'monthly_sales': monthly_sales,
                           'weekly_sales': weekly_sales, 'user_count': user_count, 'total_income': total_income,
                           'order_count': order_count, 'product_count': product_count, 'payment': payment})
