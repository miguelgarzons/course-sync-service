
from rest_framework.views import APIView
from rest_framework.response import Response
from course_sync_service.app.create_courses.infrastructure.docs.docs import crear_cursos_schema,obtener_cursos_schema
from course_sync_service.app.create_courses.infrastructure.input.serializers import MoodleQueryParamsSerializer


class CreateCourseAPIView(APIView):
    @crear_cursos_schema()
    def post(self, request, *args, **kwargs):
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
    @obtener_cursos_schema()
    def get(self, request, *args, **kwargs):
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