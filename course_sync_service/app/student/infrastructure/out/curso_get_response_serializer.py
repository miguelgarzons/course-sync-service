from rest_framework import serializers


class CourseFormatOptionSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class CustomFieldSerializer(serializers.Serializer):
    name = serializers.CharField()
    shortname = serializers.CharField()
    type = serializers.CharField()
    valueraw = serializers.CharField(allow_blank=True)
    value = serializers.CharField(allow_blank=True, allow_null=True)


class CursoGetResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    shortname = serializers.CharField()
    categoryid = serializers.CharField()
    categorysortorder = serializers.CharField()
    fullname = serializers.CharField()
    displayname = serializers.CharField()
    idnumber = serializers.CharField()
    summary = serializers.CharField()
    summaryformat = serializers.CharField()
    format = serializers.CharField()
    showgrades = serializers.CharField()
    newsitems = serializers.CharField()
    startdate = serializers.CharField()
    enddate = serializers.CharField()
    numsections = serializers.CharField()
    maxbytes = serializers.CharField()
    showreports = serializers.CharField()
    visible = serializers.CharField()
    hiddensections = serializers.CharField()
    groupmode = serializers.CharField()
    groupmodeforce = serializers.CharField()
    defaultgroupingid = serializers.CharField()
    timecreated = serializers.CharField()
    timemodified = serializers.CharField()
    enablecompletion = serializers.CharField()
    completionnotify = serializers.CharField()
    lang = serializers.CharField()
    forcetheme = serializers.CharField()

    courseformatoptions = CourseFormatOptionSerializer(many=True)
    customfields = CustomFieldSerializer(many=True)

    showactivitydates = serializers.CharField()
    showcompletionconditions = serializers.CharField()
