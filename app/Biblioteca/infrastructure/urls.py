from django.urls import path

from .views import BibliotecaView

urlpatterns = [
    path("", BibliotecaView.as_view(), name="biblioteca"),
   
]
