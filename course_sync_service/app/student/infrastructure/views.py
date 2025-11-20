
from rest_framework.views import APIView
from rest_framework.response import Response
from course_sync_service.app.courses.infrastructure.input.serializers import MoodleQueryParamsSerializer
from course_sync_service.app.student.infrastructure.docs.docs import *
from course_sync_service.app.student.infrastructure.input.delete_params_serializer import MoodleDeleteParamsSerializer
from course_sync_service.app.student.infrastructure.input.get_params_serializer import MoodleGetParamsSerializer
from course_sync_service.app.student.infrastructure.input.serializers import MoodleEnrolmentParamsSerializer
from course_sync_service.app.student.infrastructure.out.curso_create_response_serializer import CursoGoogleResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from course_sync_service.app.student.infrastructure.out.curso_get_response_serializer import CursoGetResponseSerializer
from course_sync_service.app.shared.container import container

class StudentAPIView(APIView):


    @obtener_estudiantes_schema()
    def get(self, request, *args, **kwargs):
        serializer = MoodleGetParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            use_case = container.course().list()
            result = use_case.ejecutar(validated_data)            
            response_serializer = CursoGetResponseSerializer(result, many=isinstance(result, list))
            return Response({"status": "success","data": response_serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)
            

        
    @crear_estudiantes_schema()
    def post(self, request, *args, **kwargs):
        serializer = MoodleEnrolmentParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            use_case = container.course().create()
            result = use_case.ejecutar(validated_data)
            response_serializer = CursoGoogleResponseSerializer(result, many=isinstance(result, list))
            return Response({"status": "success","data": response_serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)
        


    @eliminar_estudiantes_schema()
    def delete(self, request, *args, **kwargs):
        serializer = MoodleDeleteParamsSerializer(data=request.query_params)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            use_case = container.course().delete()
            result = use_case.ejecutar(validated_data)            
            response_serializer = CursoDeleteResponseSerializer(result, many=isinstance(result, list))
            return Response({"status": "success","data": response_serializer.data})
        return Response({"status": "error", "errors": serializer.errors}, status=400)
            
    @actualizar_estudiantes_schema()
    def put(self, request, *args, **kwargs):
        serializer = MoodleQueryParamsSerializer(data=request.query_params)
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            courses = validated_data.get('courses', [])
            
            return Response({
                "status": "ok", 
                "data": validated_data,
                "courses_count": len(courses)
            })
        else:
            return Response({
                "status": "error", 
                "errors": serializer.errors
            }, status=400)