# -*- encoding: utf-8 -*-
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
from product.models import Product, Upholstery
# Create your views here.
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from cart.models import Cart


def index(request):
    return render(request,'index.html')

def index2(request):
    return render(request,'index2.html')

def index3(request):
    return render(request,'index3.html')


def about(request):
    return render(request,'about.html')


def agents(request):
    return render(request, 'agents.html')


def fairs(request):
    return render(request, 'fairs.html')


def contact(request):
    form = ContactForm()
    context = {
        "form": form
    }

    if request.method == "POST":
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


def upholstery(request):
    cart_list = []
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        for x in cart.upholsteries.all():
            cart_list.append(x.id)
        context = {'cart': cart}

    query = request.GET
    upholsteries = Upholstery.objects.all()

    if query:
        if query['renk'] != "Hepsi":
            upholsteries = Upholstery.objects.filter(renk=query['renk']).all()

    return render(request, 'upholstery.html', {'upholstery': upholsteries, 'cart': cart_list})

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

    query = request.POST
    products = Product.objects.all()

    if query:
        product = Product.objects.all()
        if request.POST.get('desen'):
            product = product.filter(desen=query['desen'])
        if request.POST.get('renk'):
            product = product.filter(renk=query['renk'])
        if request.POST.get('agirlik'):
            product = product.filter(agirlik=query['agirlik'])
        if request.POST.get('karisim'):
            product = product.filter(karisim=query['karisim'])
        if request.POST.get('siparis'):
            product = product.filter(karisim=query['siparis'])


        products = product

    return render(request,'products.html',{'products':products,'cart':cart_list})


@login_required
def carts(request):
    template = 'cart.html'
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:
        cart = Cart.objects.get(id=the_id)
        det_ins = list(cart.products.all().values_list('id', flat=True))
        if type(cart.details) != dict:
            det = json.loads(cart.details)
        else:
            det = cart.details

        if type(cart.details) != dict:
            siparisler = json.loads(cart.details)
        else:
            siparisler = cart.details

        det_keys = map(int, list(det.keys()))
        status = False
        if set(det_ins).issubset(det_keys):
            status = True
        context = {'cart': cart, 'details': siparisler, "status": status}
        if request.method == "POST":
            istekler = []
            dosemelik = []
            for x in cart.products.all():
                istekler.append(x.name)
            for y in cart.upholsteries.all():
                istekler.append(y.name)
                dosemelik.append(y.name)
            user = ExtendedUser.objects.filter(email=request.user.email).all()

            msg_html = render_to_string('email.html', {'urunler': istekler, 'alici': user[0].username, 'siparis': siparisler, 'dosemelik': dosemelik })
            msg_html2 = render_to_string('email2.html', {'urunler': istekler, 'alici': user[0].username, 'siparis': siparisler, 'dosemelik': dosemelik  })
            send_mail("Yeni bir siparis var ",
                      "Siparis!",
                      "ardasoylu39@gmail.com",
                      ["ardasoylu39@gmail.com"],
                      html_message=msg_html,
                      )
            send_mail("Yeni bir siparis verdiniz ",
                      "Siparis!",
                      "ardasoylu39@gmail.com",
                      [user[0].email],
                      html_message=msg_html2,
                      )

            messages.add_message(request, messages.SUCCESS, 'Siparişiniz mail adresinize gönderildi.')
            return redirect('products')

    else:
        message = "Alışveriş listeniz boş"
        context = {"empty": True, "emptymessage": message}

    return render(request,template,context)



def update_carts(request,slug):
    request.session.set_expiry(9000)
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


    request.session['items_total'] = cart.upholsteries.count() + cart.products.count()

    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse('products'))


def update_carts_2(request,slug):
    request.session.set_expiry(9000)
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
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not products in cart.products.all():
        cart.products.add(products)
    else:
        cart.products.remove(products)
        new_details = json.loads(cart.details)
        del new_details[slug]
        cart.details = new_details

    new_total = 0.00
    for item in cart.products.all():
        new_total += float(item.price)


    request.session['items_total'] = cart.upholsteries.count() + cart.products.count()
    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse('products'))

import json

def update_carts_3(request):
    request.session.set_expiry(9000)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    cart = Cart.objects.get(id=the_id)

    if request.method == "POST":
        cart = Cart.objects.filter(id=the_id).all()
        for x in cart:

            if type(x.details) != dict:
                details = json.loads(x.details)
            else:
                details = x.details

            if request.POST.get('urun_id') in details.keys():
                details[int(Product.objects.filter(id=request.POST.get('urun_id'))[0].id)] = {"id":int(request.POST.get('urun_id')), "desen":request.POST.get('desen'),"renk": request.POST.get('renk'),"karisim": request.POST.get('karisim'), "agirlik": request.POST.get('agirlik'),"siparis": request.POST.get('siparis')}
            else:
                details[int(Product.objects.filter(id=request.POST.get('urun_id'))[0].id)] = {"id":int(request.POST.get('urun_id')),"desen":request.POST.get('desen'),"renk": request.POST.get('renk'),"karisim": request.POST.get('karisim'), "agirlik": request.POST.get('agirlik'),"siparis": request.POST.get('siparis')}

            cart.update(details=json.dumps(details))
        return HttpResponseRedirect(reverse('carts'))

    cart.save()
    return HttpResponseRedirect(reverse('carts'))


def update_carts_up(request,slug):
    request.session.set_expiry(9000)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id


    cart = Cart.objects.get(id=the_id)
    try:
        upholsteries = Upholstery.objects.get(id=slug)
    except Upholstery.DoesNotExist:
        pass
    except:
        pass
    if not upholsteries in cart.upholsteries.all():
        cart.upholsteries.add(upholsteries)
    else:
        cart.upholsteries.remove(upholsteries)

    request.session['items_total'] = cart.upholsteries.count() + cart.products.count()

    cart.save()
    return HttpResponseRedirect(reverse('upholstery'))


def update_carts_up_2(request,slug):
    request.session.set_expiry(9000)
    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id


    cart = Cart.objects.get(id=the_id)
    try:
        upholsteries = Upholstery.objects.get(id=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass
    if not upholsteries in cart.upholsteries.all():
        cart.upholsteries.add(upholsteries)
    else:
        cart.upholsteries.remove(upholsteries)

    request.session['items_total'] = cart.upholsteries.count() + cart.products.count()
    cart.save()
    return HttpResponseRedirect(reverse('upholstery'))



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Hesabınızı aktifleştirin.'
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

            return HttpResponse('Hesabınızı etkinleştirmek için lütfen mail adresinizi onaylayın.')
    else:
        form = SignupForm()
    return render(request, 'registration/register.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Şifreniz başarıyla güncellendi.')
            return redirect('change_password')
        else:
            messages.error(request, 'Lütfen hatalara dikkat edin!')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/accounts/password_change_form.html', {
        'form': form
    })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = ExtendedUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return HttpResponse('Aktivasyon linki geçerli değil')