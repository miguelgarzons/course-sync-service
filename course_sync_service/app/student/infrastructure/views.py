
from rest_framework.views import APIView
from rest_framework.response import Response

class StudentAPIView(APIView):

    def post(self, request, *args, **kwargs):

        return Response({"status": "error"}, status=400)
        
