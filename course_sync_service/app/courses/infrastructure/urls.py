from django.urls import path

from .views import CreateCourseAPIView

urlpatterns = [
    path("", CreateCourseAPIView.as_view(), name="Acta_crear"),
   
]
