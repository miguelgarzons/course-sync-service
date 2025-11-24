from course_sync_service.app.courses.domain.entities import Curso


class CursoMoodleMapper:
    @staticmethod
    def from_validated_data(data: dict) -> list[Curso]:
        cursos = []
        for c in data.get("courses", []):
            cursos.append(Curso(
                id=c.get("id"),               
                fullname=c.get("fullname"),
                shortname=c.get("shortname"),
                categoryid=c.get("categoryid"),
                startdate=c.get("startdate"),
                enddate=c.get("enddate"),
                visible=c.get("visible"),
            ))
        return cursos
