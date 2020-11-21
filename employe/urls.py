from django.urls import path

from . import views

app_name = 'employe'

urlpatterns = [
     path('employe/', views.employe, name='employe'),
     path('message/', views.message, name='message'),
     path('boite-reception', views.get_messages, name='get_messages'),
     path('boite-reception/<int:id_message>/reponse', views.reponse_message, name='reponse_message'),
     path('message/save', views.save_message, name='save_message'),

]