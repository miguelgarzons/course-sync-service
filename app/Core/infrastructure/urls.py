from django.urls import path

from .views import GenerarLLaveMaestraView, DescargarCarpetaView,EmailTokenView

urlpatterns = [
    path(
        "GenerarLLaveMaestraView/",
        GenerarLLaveMaestraView.as_view(),
        name="Generar LLave Maestra",
    ),
 path("descargar/<str:llave>/", DescargarCarpetaView.as_view(), name="descargar_carpeta"),
 path('token/email/', EmailTokenView.as_view(), name='token_by_email'),

]
