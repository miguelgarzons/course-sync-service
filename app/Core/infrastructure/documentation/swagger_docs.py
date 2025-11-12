from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from ..serializers import GenerarDocumentoSerializer

crear_acta_swagger = swagger_auto_schema(
    operation_description="Crea un nuevo acta en el sistema.",
    tags=["Core"],
)
