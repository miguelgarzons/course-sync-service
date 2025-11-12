from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from app.Biblioteca.infrastructure.input.serializers import EtiquetasDinamicasSerializer,BibliotecaQuerySerializer
from app.Biblioteca.infrastructure.out.serializers import BibliotecaDetailResponseSerializer, BibliotecaResponseSerializer
from .docs.acta_docs import crear_acta_doc, obtener_acta_doc
from app.shared.container import container
from rest_framework_simplejwt.authentication import JWTAuthentication
from app.shared.auth.permissions import HasGroupPermission
class ActaPermission(HasGroupPermission):
    allowed_groups = ['admin'] 
    method_groups = {
        'POST': ['admin'],     
        'GET': ['admin', 'Editor', 'Coordinador']  
    }

class BibliotecaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [ActaPermission]
 
    def post(self, request):
        serializer = EtiquetasDinamicasSerializer(data=request.data)
        if serializer.is_valid():
            use_case = container.biblioteca().crear_biblioteca()  
            biblioteca_entity = use_case.ejecutar(**serializer.validated_data)
            response_serializer = BibliotecaResponseSerializer(biblioteca_entity)
            return Response(
                {
                    "message": "Acta creada exitosamente",
                    "data": response_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    def get(self, request):
        serializer = BibliotecaQuerySerializer(data=request.GET)
        if serializer.is_valid():
            try:
                use_case = container.biblioteca().obtener_biblioteca()
                biblioteca_entity = use_case.ejecutar(**serializer.validated_data)
                response_serializer = BibliotecaDetailResponseSerializer(biblioteca_entity)
                return Response(
                    {
                        "message": "Biblioteca obtenida exitosamente",
                        "data": response_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
                
                
