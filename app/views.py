from django.shortcuts import render
from .forms import ContactForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from product.models import Product

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    form = ContactForm()
    context = {"form": form}

    if request.method == "POST":
        my_form = ContactForm(request.POST)
        if my_form.is_valid():
            msg_html = render_to_string('email3.html', {
                'name': request.POST['name'], 
                'email': request.POST['email'],
                'content': request.POST['content'],
                'phone': request.POST['phone']
            })
            message = f"<p><strong>{request.POST['name']}</strong> mesaj gönderdi: {request.POST['content']} İletişim: {request.POST['email']} - {request.POST['phone']}</p>"
            
            send_mail(
                "Yeni İletişim Mesajı",
                message,
                "contact@organikurunler.com",
                ["admin@organikurunler.com"],
                html_message=msg_html,
            )
    return render(request, 'contact.html', context)

def products(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products.html', {'products': products})