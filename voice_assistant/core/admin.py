from django.contrib import admin
from .models import AppCommand, VoiceResponse
# Register your models here.
admin.site.register([AppCommand, VoiceResponse]) # для редакции бази данних (регистрация админ панели для подальшого изменения через адним панель)
