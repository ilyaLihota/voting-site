from django.urls import path

from poll import views


urlpatterns = [
    path('', views.polls_list, name='polls_list_url'),
    path('accounts/<int:user_id>/', views.account, name='account_url'),
    path('polls/<int:id>/', views.PollDetail.as_view(), name='poll_detail_url'),
    path('polls/create/<int:user_id>/', views.poll_create, name='poll_create_url'),
    path('polls/update/<int:poll_id>/', views.PollUpdate.as_view(), name='poll_update_url'),
    path('polls/delete/<int:poll_id>/', views.PollDelete.as_view(), name='poll_delete_url'),

    path('questions/<int:question_id>/', views.QuestionDetail.as_view(), name='question_detail_url'),
    path('<int:poll_id>/question_choices/create/', views.manage_question, name='question_choices_create_url'),

    # path('take_poll/<int:poll_id>/', views.TakePoll.as_view(), name='take_poll_url'),

    path('search/', views.search, name='search'),
]
