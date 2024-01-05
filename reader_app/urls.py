from django.urls import path
from . import views

app_name = 'reader_app'
urlpatterns = [
    # Homepage.
    path('', views.index, name='index'),
    # Other.
    path('<path:path>', views.other, name='other'),
]
