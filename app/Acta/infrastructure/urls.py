from django.urls import path

from .views import ActaView

urlpatterns = [
    path("", ActaView.as_view(), name="Acta_crear"),
   
]
