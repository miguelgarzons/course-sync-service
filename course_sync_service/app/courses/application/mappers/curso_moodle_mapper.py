
from course_sync_service.app.courses.domain.entities import Curso


class CursoMoodleMapper:
    @staticmethod
    def from_validated_data(data: dict) -> list[Curso]:
        cursos = []
        for c in data.get("courses", []):
            cursos.append(Curso(
                id=c["id"],
                fullname=c["fullname"],
                shortname=c["shortname"],
                categoryid=c["categoryid"],
                startdate=c["startdate"],
                enddate=c["enddate"],
                visible=c["visible"],
            ))
        return cursos
    
    
