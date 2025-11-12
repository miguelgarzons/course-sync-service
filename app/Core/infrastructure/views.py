import shutil
import tempfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .documentation.swagger_docs import crear_acta_swagger
from django.http import FileResponse, Http404
import os
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import EmailTokenSerializer, RegistroCalificadoEntitySerializer
from app.shared.container import container


class GenerarLLaveMaestraView(APIView):
    def get(self, request, *args, **kwargs):
        use_case = container.core().obtener_llave()
        registros = use_case.ejecutar()
        serializer = RegistroCalificadoEntitySerializer(registros, many=True)
        return Response(serializer.data)
        
    


class DescargarCarpetaView(APIView):
    """
    Descarga una carpeta completa desde 'output/' según la llave.
    """

    def get(self, request, llave):

        carpeta_path = os.path.join("output", llave)

        if not os.path.exists(carpeta_path):
            print("❌ Carpeta no encontrada en:", carpeta_path)  
            raise Http404("Carpeta no encontrada")

        temp_dir = tempfile.mkdtemp()
        zip_filename = f"{llave}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        shutil.make_archive(zip_path[:-4], 'zip', carpeta_path)
        response = FileResponse(open(zip_path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{zip_filename}"'
        return response


class EmailTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        User = get_user_model()
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)