from django.urls import path
from . import views

app_name = 'reader_app'
urlpatterns = [
    # Homepage.
    path('', views.index, name='index'),
]
