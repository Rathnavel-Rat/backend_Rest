from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('registration', views.Register.as_view(), name="register"),
    path('emailVerification/', views.VerfiyUsingEmail.as_view(), name="emailVerification"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("login",views.LoginApiView.as_view(),name="login"),
    path("logout",views.LogoutAPIView.as_view(),name="logout"),

    path('RequestPasswordChange',views.RequestChangingPassword.as_view(),name="requestpasswordchange"),
    path("RequestPasswordChangeVerification/<uidb64>/<token>",views.RequestPasswordChangeEmailVerifiacation.as_view(),name="RECV"),
    path("SetNewPassword",views.SetNewPasswordApi.as_view(),name="setNewPassword")


]
