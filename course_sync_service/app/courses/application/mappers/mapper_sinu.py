from typing import Any, Dict


class CursoSinuMapper:

    @staticmethod
    def from_validated_data(resultados):
        cursos_sinu = []
        for item in resultados:
            curso = {
                "id": item.get("course_id"),
                "shortname": item.get("name")
            }
            cursos_sinu.append(curso)
        return cursos_sinu
    
    @staticmethod
    def map_course(google_course: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "id": str(google_course.get("id", "")),
            "shortname": google_course.get("section", "") or "",
            "categoryid": "",
            "categorysortorder": "",
            "fullname": google_course.get("name", "") or "",
            "displayname": google_course.get("name", "") or "",
            "idnumber": "",
            "summary": google_course.get("description", "") or "",
            "summaryformat": "",
            "format": "",
            "showgrades": "",
            "newsitems": "",
            "startdate": "",
            "enddate": "",
            "numsections": "",
            "maxbytes": "",
            "showreports": "",
            "visible": "1" if google_course.get("courseState") == "ACTIVE" else "",
            "hiddensections": "",
            "groupmode": "",
            "groupmodeforce": "",
            "defaultgroupingid": "",
            "timecreated": google_course.get("creationTime", "") or "",
            "timemodified": google_course.get("updateTime", "") or "",
            "enablecompletion": "",
            "completionnotify": "",
            "lang": "",
            "forcetheme": "",
            "courseformatoptions": [],
            "showactivitydates": "",
            "showcompletionconditions": "",
            "customfields": []
        }