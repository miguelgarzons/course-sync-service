from course_sync_service.app.courses.domain.entities import Curso

class CursoGoogleMapper:

    @staticmethod
    def to_google_format(curso: Curso) -> dict:
        """Convierte un Curso (dominio) al formato esperado por Google Classroom."""
        return {
            "name": curso.fullname,
            "section": curso.shortname,
            "descriptionHeading": curso.fullname,
            "description": f"Curso migrado desde Moodle (ID categoría {curso.categoryid})",
            "room": "",
            "ownerId": "me",
            "courseState": "PROVISIONED",
        }
