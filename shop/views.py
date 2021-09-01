from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Products, Contact, Orders, OrderUpdate, Users
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum
import json
from random import randint
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

MERCHANT_KEY = 'bKMfNxPPf_QdZppa'
# Create your views here.


def home(request):
    count = Products.objects.count()
    featured = []
    for i in range(3):
        random_object = Products.objects.all()[randint(0, count - 1)]
        featured.append(random_object)
    return render(request, 'shop/Home.html', {'products': featured})


def index(request):
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/hello.html', params)


def about(request):
    return render(request, 'shop/about.html')


@csrf_protect
def contact(request):
    if request.method == "POST":
        name = request.POST.get('username', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        return JsonResponse({
            "success": True,
            'message': 'Submitted Successfully'
        })
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        order = Orders.objects.filter(order_id=orderId, email=email)
        if len(order) > 0:
            update = OrderUpdate.objects.filter(order_id=orderId)
            updates = []
            for item in update:
                updates.append({
                    'text': item.update_desc,
                    'time': item.timestamp
                })
                response = json.dumps(updates, default=str)
            return HttpResponse(response)
        else:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')


def searchMatch(query, item):
    # return true only if query matches the item
    if query.lower() in item.desc.lower() or query in item.product_name.lower(
    ) or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Products.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)


def productView(request, myid):

    # Fetch the product using the id
    product = Products.objects.filter(id=myid)
    return render(request, 'shop/prodView.html', {'product': product[0]})


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get(
            'address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json,
                       name=name,
                       email=email,
                       address=address,
                       city=city,
                       state=state,
                       zip_code=zip_code,
                       phone=phone,
                       amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {
            'MID': 'DIY12386817555501617',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    global checksum
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html',
                  {'response': response_dict})


@csrf_protect
def signup(request):
    messagee = ""
    if request.method == 'POST':
        user_name = request.POST.get('username', '')
        user_email = request.POST.get('email', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('confirm_password', '')

        if password1 != password2:
            messagee = "Password Do not Matched!"
            return JsonResponse({
                "success": False,
                'message': messagee,
            })

        if len(password1) < 9:
            messagee = "Length of password should be greater than 9"
            return JsonResponse({
                "success": False,
                'message': messagee,
            })

        # if not user_name.isalnum():
        #     messagee = "Username should only contain integers and alphabets"
        #     return JsonResponse({
        #         "success": False,
        #         'message': messagee,
        #     })

        info = Users(
            user_name=user_name,
            user_email=user_email,
        )
        info.save()
        if User.objects.filter(username=user_name).exists():
            messagee = "Username already in use"
            return JsonResponse({
                "username": user_name,
                "success": False,
                'message': messagee,
            })
        else:
            myuser = User.objects.create_user(username=user_name,
                                              email=user_email,
                                              password=password1)
            myuser.save()
            return JsonResponse({
                "success": True,
                'message': 'You are Successfully Signed up '
            })

    return render(request, 'shop/signup.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' +
                  response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html',
                  {'response': response_dict})


def logins(request):
    thank = True
    if request.method == "POST":
        user = request.POST.get('username')
        password = request.POST.get('password')
        print("username:", end="")
        print(user)
        user = authenticate(username=user, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'shop/login.html', {'thank': thank})

    return render(request, 'shop/login.html')


def logouts(request):
    logout(request)
    return redirect('/')
