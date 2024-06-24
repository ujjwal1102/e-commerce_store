import random, datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP
from users.models import User
from .serializers import UserSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404
def send_otp_email(email):
    otp = random.randint(100000, 999999)
    subject = "Verification OTP"
    message = f"Your OTP is {otp}."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return otp


def verify_otp(email, otp):
    otp_obj = get_object_or_404(OTP, email=email)
    dt = timezone.now()
    otp_valid_duration = datetime.timedelta(minutes=1)
    if int(otp_obj.otp) == int(otp) and ((dt - otp_obj.created_at) <= otp_valid_duration):
        otp_obj.delete()  # Delete OTP only when it is correct
        return True
    else:
        return False

