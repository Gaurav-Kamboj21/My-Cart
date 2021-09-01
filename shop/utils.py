from django.core.mail import send_mail
from django.conf import settings


def email(request):
    subject = 'My cart'
    message = 'Track Your order {} here'.format('http://127.0.0.1:8000/tracker/')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['csecec.gaurav1702635@gmail.com']
    send_mail(subject, message, email_from, recipient_list)
