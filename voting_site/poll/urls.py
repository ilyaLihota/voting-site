from django.urls import path

from poll import views


urlpatterns = [
    path('', views.polls_list, name='polls_list_url'),
    path('polls/<int:id>', views.PollDetail.as_view(), name='poll_detail_url'),
    path('polls/create/', views.poll_create, name='poll_create_url'),
    path('search/', views.search, name='search'),
    path('account/', views.account, name='account'),
]
