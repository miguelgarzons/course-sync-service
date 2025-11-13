from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from .docs.acta_docs import crear_acta_doc, obtener_acta_doc
from course_sync_service.app.shared.container import container
from course_sync_service.app.shared.auth.permissions import HasGroupPermission


class ActaPermission(HasGroupPermission):
    allowed_groups = ['admin'] 
    method_groups = {
        'POST': ['admin'],     
        'GET': ['admin', 'Editor', 'Coordinador']  
    }

class ActaView(APIView):

    @swagger_auto_schema(**crear_acta_doc)
    def post(self, request):

            return Response(
                {
                    "message": "Acta creada exitosamente",
                    "data": "response_serializer.data",
                },
                status=status.HTTP_201_CREATED,)

 