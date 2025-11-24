from rest_framework import serializers


class TeacherFolderSerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    title = serializers.CharField(required=False, allow_null=True)
    alternateLink = serializers.CharField(required=False, allow_null=True)


class GradeCategorySerializer(serializers.Serializer):
    id = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    weight = serializers.IntegerField(required=False, allow_null=True)
    defaultGradeDenominator = serializers.IntegerField(required=False, allow_null=True)


class GradebookSettingsSerializer(serializers.Serializer):
    calculationType = serializers.CharField(required=False, allow_null=True)
    displaySetting = serializers.CharField(required=False, allow_null=True)
    gradeCategories = GradeCategorySerializer(many=True, required=False, allow_null=True)


class CursoUpdateResponseSerializer(serializers.Serializer):
    # Campos ya presentes en Google
    course_id = serializers.CharField()

    id = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    section = serializers.CharField(required=False, allow_null=True)
    descriptionHeading = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    ownerId = serializers.CharField(required=False, allow_null=True)
    creationTime = serializers.CharField(required=False, allow_null=True)
    updateTime = serializers.CharField(required=False, allow_null=True)
    enrollmentCode = serializers.CharField(required=False, allow_null=True)
    courseState = serializers.CharField(required=False, allow_null=True)
    alternateLink = serializers.CharField(required=False, allow_null=True)
    teacherGroupEmail = serializers.CharField(required=False, allow_null=True)
    courseGroupEmail = serializers.CharField(required=False, allow_null=True)
    teacherFolder = TeacherFolderSerializer(required=False, allow_null=True)
    guardiansEnabled = serializers.BooleanField(required=False, allow_null=True)

    # Este no estaba antes → LO AGREGAMOS
    calendarId = serializers.CharField(required=False, allow_null=True)

    gradebookSettings = GradebookSettingsSerializer(required=False, allow_null=True)

    # Objeto crudo por si lo quieres ver completo
    raw_data = serializers.DictField(required=False)
