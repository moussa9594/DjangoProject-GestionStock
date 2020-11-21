from django.urls import path

from . import views
from employe import views as views_employe

app_name = 'authenticate'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('login/update-password', views.change_pwd, name='change_pwd'),
    path('logout/', views.logout, name='logout'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]