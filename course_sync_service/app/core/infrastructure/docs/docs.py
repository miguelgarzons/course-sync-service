from drf_spectacular.utils import (
    extend_schema, 
    OpenApiParameter, 
    OpenApiResponse,
    OpenApiExample
)
from drf_spectacular.types import OpenApiTypes
from ..out.curso_get_response_serializer import CursoGetResponseSerializer
from ..out.curso_delete_response_serializer import CursoDeleteResponseSerializer
from ..out.curso_create_response_serializer import CursoGoogleResponseSerializer


def core_api_post_schema():
    """
    Schema principal para el endpoint CoreAPIView.
    Documenta todas las operaciones disponibles mediante wsfunction.
    """
    return extend_schema(
        operation_id="execute_moodle_function",
        summary="Ejecutar operaciones de Moodle Web Services",
        description=(
            "Endpoint unificado que ejecuta diferentes operaciones según el parámetro `wsfunction`.\n\n"
            "**Operaciones disponibles:**\n"
            "- `core_course_create_courses`: Crear cursos\n"
            "- `core_course_get_courses`: Obtener cursos\n"
            "- `core_course_update_courses`: Actualizar cursos\n"
            "- `core_course_delete_courses`: Eliminar cursos\n\n"
            "Los parámetros adicionales dependen de la operación seleccionada. "
            "Ver ejemplos en la sección de responses."
        ),
        tags=["Core API"],
        parameters=[
            OpenApiParameter(
                name="wstoken",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Token de autenticación de Moodle",
                required=True,
                examples=[
                    OpenApiExample(
                        name="Token ejemplo",
                        value="abc123def456"
                    )
                ]
            ),
            OpenApiParameter(
                name="wsfunction",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description=(
                    "Función del web service a ejecutar. Determina qué operación se realizará "
                    "y qué parámetros adicionales son requeridos."
                ),
                required=True,
                enum=[
                    "core_course_create_courses",
                    "core_course_get_courses",
                    "core_course_update_courses",
                    "core_course_delete_courses"
                ]
            ),
            OpenApiParameter(
                name="moodlewsrestformat",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Formato de respuesta (json, xml)",
                required=False,
                enum=["json", "xml"]
            ),
        ],
        responses={
            200: OpenApiResponse(
                description=(
                    "Operación exitosa. La estructura de respuesta depende de wsfunction:\n\n"
                    "**create_courses**: Retorna el curso creado con su ID\n"
                    "**get_courses**: Retorna lista de cursos\n"
                    "**update_courses**: Retorna confirmación de actualización\n"
                    "**delete_courses**: Retorna confirmación de eliminación"
                )
            ),
            400: OpenApiResponse(
                description="Parámetros inválidos o wsfunction no soportado"
            ),
            404: OpenApiResponse(
                description="Recurso no encontrado (para operaciones get, update, delete)"
            ),
        },
        examples=[
            OpenApiExample(
                name="Crear curso",
                description="Ejemplo de creación de curso",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "core_course_create_courses",
                    "courses[0][fullname]": "Matemáticas Avanzadas",
                    "courses[0][shortname]": "MAT-ADV",
                    "courses[0][categoryid]": "1"
                }
            ),
            OpenApiExample(
                name="Obtener cursos",
                description="Ejemplo de consulta de cursos",
                value={
                    "wstoken": "abc123",
                    "wsfunction": "core_course_get_courses",
                    "options[ids][0]": "123"
                }
            )
        ]
    )