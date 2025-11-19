from course_sync_service.app.courses.domain.entities import CursosAEliminar


class MoodleDeleteMapper:

    @staticmethod
    def from_validated_data(data):
        """
        Convierte los datos del serializer DRF a la entidad de dominio.
        """
        ids = data["options"]["ids"]
        return CursosAEliminar(ids=ids)
