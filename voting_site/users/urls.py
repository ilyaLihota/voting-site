from django.urls import path

from users import views


urlpatterns = [
    path('login/', views.login_view, name='login_url'),
    path('logout/', views.logout_view, name='logout_url'),
    path('register/', views.register, name='register_url'),
    path('verify/', views.verify_email),
]
