from django.db import models
from django.urls import reverse

class MenuItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название пункта")
    menu_name = models.CharField(max_length=255, verbose_name="Название меню") # Для нескольких меню
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', verbose_name="Родительский пункт", on_delete=models.CASCADE)
    url = models.CharField(max_length=255, blank=True, verbose_name="URL (явный или named url)")
    named_url = models.CharField(max_length=255, blank=True, verbose_name="Имя URL (named url)")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    def get_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except:
                return '#'  
        elif self.url:
            return self.url
        else:
            return '#'  

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
