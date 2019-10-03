from django.urls import path

from users import views


urlpatterns = [
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view),
    path('register/', views.register, name='register'),
    path('verify/', views.verify_email),
]
