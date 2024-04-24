import random
from django.core.mail import send_mail
from django.conf import settings

def send_otp_email(email):
    otp = random.randint(100000, 999999)
    subject = 'Verification OTP'
    message = f'Your OTP is {otp}.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return otp

def verify_otp(email, otp):
    # Here you can check if the OTP entered by the user matches the OTP sent to the email
    # You might want to use some caching mechanism or store OTP in database for verification
    return True  # Replace this with your logic for OTP verification
