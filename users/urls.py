
from django.urls import path
from . import views

urlpatterns = [
    path('login/', view=views.LoginAPIView.as_view()),
    path('logout/', view=views.LogoutView.as_view()),
    path('user/', view=views.UserView.as_view()),
    path('register/', view=views.RegisterAPIView.as_view()),
    path('profile/', view=views.CustomerView.as_view()),
    # path('profile/update', view=views.CustomerView.as_view()),

]
