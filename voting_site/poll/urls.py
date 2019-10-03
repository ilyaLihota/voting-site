from django.urls import path

from poll import views


urlpatterns = [
    path('', views.polls_list),
    path('polls/<int:id>', views.poll_detail, name='detail'),
]
