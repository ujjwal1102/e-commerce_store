
from django.urls import path, include
from . import views





urlpatterns = [
    path('login/', view=views.LoginAPIView.as_view()),
    path('logout/', view=views.LogoutView.as_view()),
    path('user/', view=views.UserView.as_view()),
    path('register/', view=views.RegisterAPIView.as_view()),
    path('register/otp', view=views.OTPVerify.as_view()),
    path('profile/', view=views.CustomerView.as_view()),   

]
