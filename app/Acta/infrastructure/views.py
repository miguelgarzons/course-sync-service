from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from app.Acta.infrastructure.out.serializers import ActaDetailResponseSerializer, ActaResponseSerializer
from app.Acta.infrastructure.input.serializers import  ActaQuerySerializer, EtiquetasDinamicasSerializer
from .docs.acta_docs import crear_acta_doc, obtener_acta_doc
from app.shared.container import container
from app.shared.auth.permissions import HasGroupPermission

class ActaPermission(HasGroupPermission):
    allowed_groups = ['admin'] 
    method_groups = {
        'POST': ['admin'],     
        'GET': ['admin', 'Editor', 'Coordinador']  
    }

class ActaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ActaPermission]

    @swagger_auto_schema(**crear_acta_doc)
    def post(self, request):
        serializer = EtiquetasDinamicasSerializer(data=request.data)
        if serializer.is_valid():
            use_case = container.acta().crear_acta()
            acta_entity = use_case.ejecutar(**serializer.validated_data, creado_por=request.user)
            response_serializer = ActaResponseSerializer(acta_entity)
            return Response(
                {
                    "message": "Acta creada exitosamente",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(**obtener_acta_doc)
    def get(self, request):
        serializer = ActaQuerySerializer(data=request.GET)
        if serializer.is_valid():
            use_case = container.acta().obtener_acta()
            acta_entity = use_case.ejecutar(**serializer.validated_data)
            response_serializer = ActaDetailResponseSerializer(acta_entity)
            return Response(
                {
                    "message": "Acta obtenida exitosamente",
                    "data": response_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
