from course_sync_service.app.courses.domain.entities import Curso


class CursoGoogleUpdateMapper:

    @staticmethod
    def to_google_update_format(curso: Curso) -> dict:
        data = {}

        if curso.fullname:
            data["name"] = curso.fullname
            data["descriptionHeading"] = curso.fullname

        if curso.shortname:
            data["section"] = curso.shortname

        if curso.categoryid:
            data["description"] = f"Curso actualizado desde Moodle (ID categoría {curso.categoryid})"

        if curso.visible is not None:
            data["courseState"] = "ACTIVE" if curso.visible == 1 else "ARCHIVED"

        return data
