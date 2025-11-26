from typing import Any, Dict
from datetime import datetime

class CursoSinuMapper:

    @staticmethod
    def iso_to_unix(value: str):
        """Convierte un string ISO8601 a Unix timestamp."""
        if not value:
            return ""
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return int(dt.timestamp())
        except Exception:
            return ""

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
            "categorysortorder": "1480010",
            "fullname": google_course.get("name", "") or "",
            "displayname": google_course.get("name", "") or "",
            "idnumber": "",
            "summary": google_course.get("description", "") or "",
            "summaryformat": "1",
            "format": "tiles",
            "showgrades": "1",
            "newsitems": "5",
            "startdate": CursoSinuMapper.iso_to_unix(google_course.get("creationTime", "")),
            "enddate": CursoSinuMapper.iso_to_unix(google_course.get("updateTime", "")),
            "numsections": "13",
            "maxbytes": "1073741824",
            "showreports": "1",
            "visible": "1" if google_course.get("courseState") == "ACTIVE" else "0",
            "hiddensections": "1",
            "groupmode": "0",
            "groupmodeforce": "0",
            "defaultgroupingid": "0",
            "timecreated": CursoSinuMapper.iso_to_unix(google_course.get("creationTime", "")),
            "timemodified": CursoSinuMapper.iso_to_unix(google_course.get("updateTime", "")),
            "enablecompletion": "1",
            "completionnotify": "0",
            "lang": "es_co",
            "forcetheme": "",
            "courseformatoptions":  [
            {
                "name": "hiddensections",
                "value": 1
            },
            {
                "name": "coursedisplay", 
                "value": 1
            },
            {
                "name": "defaulttileicon",
                "value": "pie-chart"
            },
            {
                "name": "basecolour",
                "value": "#1670CC"
            },
            {
                "name": "oneimagetopics",
                "value": 0
            },
            {
                "name": "courseusesubtiles",
                "value": 0
            },
            {
                "name": "usesubtilesseczero",
                "value": 0
            },
            {
                "name": "courseshowtileprogress",
                "value": 0
            },
            {
                "name": "displayfilterbar",
                "value": 0
            },
            {
                "name": "courseusebarforheadings",
                "value": 1
            }
        ],
        "showactivitydates": False,
        "showcompletionconditions": True,
        "customfields": [
            {
                "name": "Course Duration in Hours",
                "shortname": "edwcoursedurationinhours",
                "type": "text",
                "valueraw": "",
                "value": None
            },
            {
                "name": "Course Intro Video Url (Embedded)",
                "shortname": "edwcourseintrovideourlembedded",
                "type": "text",
                "valueraw": "",
                "value": None
            },
            {
                "name": "Docente",
                "shortname": "usardocente",
                "type": "checkbox",
                "valueraw": 0,
                "value": "No"
            }
        ]
        }