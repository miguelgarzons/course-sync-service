from rest_framework import serializers


class CursoGoogleResponseSerializer(serializers.Serializer):
    course_id = serializers.CharField()
    name = serializers.CharField()
    enrollment_code = serializers.CharField(allow_null=True)
    alternate_link = serializers.CharField(allow_null=True)
 

