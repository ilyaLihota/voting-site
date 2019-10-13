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
    path('questions/create/<int:poll_id>/', views.QuestionCreate.as_view(), name='question_create_url'),
    path('questions/update/<int:question_id>/', views.QuestionUpdate.as_view(), name='question_update_url'),
    path('questions/delete/<int:question_id>/', views.QuestionDelete.as_view(), name='question_delete_url'),

    path('choices/create/<int:question_id>/', views.ChoiceCreate.as_view(), name='choice_create_url'),
    path('choices/update/<int:choice_id>/', views.ChoiceUpdate.as_view(), name='choice_update_url'),
    path('choices/delete/<int:choice_id>/', views.ChoiceDelete.as_view(), name='choice_delete_url'),

    # path('take_poll/<int:poll_id>/', views.TakePoll.as_view(), name='take_poll_url'),

    path('search/', views.search, name='search'),
]
