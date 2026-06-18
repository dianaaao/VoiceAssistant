from django.db import models

# Create your models here.
class AppCommand(models.Model):
    keyword = models.CharField(max_length = 100, verbose_name = "Keyword")
    app_name = models.CharField(max_length = 100, verbose_name = "App Name")
    path = models.CharField(max_length = 500, verbose_name = "Path", blank = True, null = True) # blank True для обозначування того що поле може буть порожнім або не обов'язковим

    def __str__(self):
        return f"Open {self.app_name}"
    
class VoiceResponse(models.Model):
    keyword = models.CharField(max_length=100, verbose_name="Keyword")
    response = models.TextField(verbose_name="Say")

    def __str__(self):
        return f"Answer for {self.keyword}"