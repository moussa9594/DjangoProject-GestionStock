from django.contrib import admin

# Register your models here.
from .models import Employe, Message

admin.site.register(Employe)
admin.site.register(Message)
