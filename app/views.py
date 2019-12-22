from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm,ContactForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from app.models import ExtendedUser
from django.core.mail import EmailMessage,send_mail
from product.models import Product
# Create your views here.
from django.urls import reverse

from cart.models import Cart



def index(request):
    return render(request,'index.html')

def index2(request):
    return render(request,'index2.html')

def index3(request):
    return render(request,'index3.html')


def about(request):
    return render(request,'about.html')


def contact(request):
    form = ContactForm()
    context = {
        "form": form
    }

    if request.method == "POST":
        print(request.POST)
        my_form = ContactForm(request.POST)
        if my_form.is_valid():
            print(my_form.cleaned_data)
        else:
            print(my_form.errors)

        msg_plain = render_to_string('email.txt', {'name': request.POST['name'], 'email': request.POST['email'],
                                                   'content': request.POST['content'],
                                                   'phone': request.POST['phone']})
        msg_html = render_to_string('email3.html', {'name': request.POST['name'], 'email': request.POST['email'],
                                                   'content': request.POST['content'],
                                                   'phone': request.POST['phone']})
        message = '<p><strong>' + request.POST['name'] + '</strong> send you a message:' + request.POST[
            'content'] + ' contact with email:' + request.POST['email'] + ' and phone. ' + request.POST[
                      'phone'] + '</p> '
        send_mail("Yeni bir mail aldınız ",
                  message,
                  "ardasoylu39@gmail.com",
                  ["ardasoylu39@gmail.com"],
                  html_message=msg_html,
                  )
    return render(request,'contact.html',context)


def products(request):
    return render(request,'products.html')

def upholstery(request):
    return render(request,'upholstery.html')

def stock_service(request):
    return render(request,'stock_service.html')


def products(request):
    cart_list = []
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        for x in cart.products.all():
            cart_list.append(x.id)
        context = {'cart':cart}


    products = Product.objects.all()
    return render(request,'products.html',{'products':products,'cart':cart_list})



def carts(request):

    template = 'cart.html'
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        context = {'cart':cart}
        if request.method == "POST":
            istekler = []
            for x in cart.products.all():
                istekler.append(x.name)
            user = ExtendedUser.objects.filter(email=request.user.email).all()

            msg_plain = render_to_string('email.txt', {'ürün': "arda"})
            msg_html = render_to_string('email.html', {'ürün': istekler, 'kişi': user[0].username})
            msg_html2 = render_to_string('email2.html', {'ürün': istekler, 'kişi': user[0].username})
            send_mail("Yeni bir sipariş var ",
                      "Sipariş!",
                      "ardasoylu39@gmail.com",
                      ["ardasoylu39@gmail.com"],
                      html_message=msg_html,
                      )
            send_mail("Yeni bir sipariş verdiniz ",
                      "Sipariş!",
                      "ardasoylu39@gmail.com",
                      [user[0].email],
                      html_message=msg_html2,
                      )
           # cart.products.all().delete()
            message = "siparişiniz mailiniz gönderildi"
            return render(request,template,{'message':message})

    else:
        message = "Alışveriş listeniz boş"
        context = {"empty":True,"emptymessage":message}




    return render(request,template,context)



def update_carts(request,slug):
    request.session.set_expiry(900)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id


    cart = Cart.objects.get(id=the_id)
    try:
        products = Product.objects.get(id=slug)
        print(products)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not products in cart.products.all():
        cart.products.add(products)
    else:
        cart.products.remove(products)

    new_total = 0.00
    for item in cart.products.all():
        new_total += float(item.price)


    request.session['items_total'] = cart.products.count()

    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse('products'))


def update_carts_2(request,slug):
    request.session.set_expiry(900)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id


    cart = Cart.objects.get(id=the_id)
    try:
        products = Product.objects.get(id=slug)
        print(products)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not products in cart.products.all():
        cart.products.add(products)
    else:
        cart.products.remove(products)

    new_total = 0.00
    for item in cart.products.all():
        new_total += float(item.price)


    request.session['items_total'] = cart.products.count()
    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse('carts'))




def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/accounts/password_change_form.html', {
        'form': form
    })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        print("here")
        user = ExtendedUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        print("here2")
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        print("here3")
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')