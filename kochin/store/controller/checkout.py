from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.decorators import login_required
from store.models import Cart, Order, OrderItem, Product, Profile
from django.contrib.auth.models import User

import random

@login_required(login_url='loginpage')
def index(request):
    rawcart = Cart.objects.filter(user=request.user)
    for item in rawcart:
        if item.product_qty > item.product.quantity :
            Cart.objects.delete(id=item.id)

    cartitems = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cartitems:
        total_price = total_price + item.product.selling_price * item.product_qty

    userprofile = Profile.objects.filter(user=request.user).first()
        
    context= {'cartitems':cartitems, 'total_price':total_price,'userprofile':userprofile}
    return render(request,'store/checkout.html',context)


@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':

        curentuser = User.objects.filter(id=request.user.id).first()

        if not curentuser.first_name:
            curentuser.first_name =request.POST.get('fname')
            curentuser.last_name = request.POST.get('lname')
            curentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.contry = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.contry = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_mode')


        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty

        neworder.total_price = cart_total_price
        trackno = 'KOCHIN'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'KOCHIN'+str(random.randint(1111111,9999999))

        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder, #here the order is the order id
                product=item.product,
                price=item.product.selling_price,
                quantity = item.product_qty
            )
            #to decrease the product qnty from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity = orderproduct.quantity - item.product_qty
            orderproduct.save()

            #To clear user's Cart
            Cart.objects.filter(user=request.user).delete()

            messages.success(request, "Your order hass been placed succesfully")

            payMode = request.POST.get('payment_mode')
            if (payMode == "Paid by PayPal"):
                return JsonResponse({'status':"Your Order placed sucessfully"})
            else:
                messages.success(request, "Your Order hass been Placed sucessfully")

    return redirect('/')



# @login_required(login_url='loginpage')
# def razorpaycheck(request):
#     cart = Cart.objects.filter(user=request.user)
#     total_price = 0
#     for item in cart:
#         total_price = total_price + item.product.selling_price * item.product_qty
#         return JsonResponse({
#             'total_price':total_price
#         })




