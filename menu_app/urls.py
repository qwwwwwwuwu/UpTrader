from django.urls import path
from . import views

urlpatterns = [
    path('my-page/', views.my_page, name='my_page'), # Пример страницы
]
