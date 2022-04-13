from django.urls import path
from .views import (
    PhoneNumberView,
    PhoneNumberVerificationView,
    SignUpView,
    LoginView,
    LogOutView,

    password_reset_phonenumber,
    password_reset_verification,
    password_reset_newpassword,

    change_password,
)

app_name = "users"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('phone/number/', PhoneNumberView.as_view(), name='phone-number-view'),
    path('phone/confirmation/<str:key>/', PhoneNumberVerificationView.as_view(), name='phone-verification'),
    path('create/account/<str:key>/', SignUpView.as_view(), name='signup-view'),

    path('reset/password/phonenumber/', password_reset_phonenumber, name='reset-password-phonenumber'),
    path('reset/password/verification/<str:key>/', password_reset_verification, name='reset-password-verification'),
    path('reset/password/newpassword/<str:key>/', password_reset_newpassword, name='reset-password-newpassword'),

    path('change/password/<int:pk>/', change_password, name='change-password'),

]