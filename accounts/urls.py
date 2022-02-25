from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
    path('login/',
          auth_views.LoginView.as_view(template_name='accounts/login.html',
                                       redirect_authenticated_user = True,
                                       redirect_field_name = 'index.html'),
          name='login'),
    path('logout/',
          auth_views.LogoutView.as_view(),
          name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
]
