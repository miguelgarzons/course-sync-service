from typing import Any, Dict
import logging

from course_sync_service.app.core.integrations.google_workspace.google_workspace_users import GoogleWorkspaceUsers

logger = logging.getLogger(__name__)


class CrearEstudiante:
    def __init__(self, google_workspace_client: GoogleWorkspaceUsers):
        self.google_workspace_client = google_workspace_client

    def ejecutar(self, validated_data) -> Dict[str, Any]:
        """
        Crea o verifica un estudiante en Google Workspace
        
        Args:
            validated_data: Diccionario con los datos validados del estudiante
                Debe contener al menos: email, firstname, lastname
        
        Returns:
            Diccionario con el resultado de la operación
        """
        logger.info(f"Iniciando creación/verificación de estudiante: {validated_data}")
        print(validated_data)
        # Validar que el email esté presente
        email = validated_data["users"][0]["email"]
        if not email:
            return {
                "success": False,
                "error": "El campo 'email' es requerido"
            }
        
        try:
            # Verificar si el usuario existe en Google Workspace
            user_exists = self.google_workspace_client.user_exists(email)
            print("gooogle-----------------------")
            print(user_exists)
            
            if user_exists:
                logger.info(f"Usuario {email} ya existe en Google Workspace")
                return {
                    "success": True,
                    "message": "El usuario ya existe en Google Workspace",
                    "email": email,
                    "action": "verified"
                }
            else:
                logger.info(f"Usuario {email} no existe en Google Workspace")
                
                # Opción 1: Solo verificar (comportamiento actual)
                return {
                    "success": False,
                    "error": "El usuario no existe en Google Workspace",
                    "email": email
                }
                
                # Opción 2: Crear el usuario automáticamente (descomenta si deseas esto)
                # return self._crear_usuario_en_google(validated_data)
        
        except Exception as e:
            logger.error(f"Error al verificar/crear estudiante {email}: {str(e)}")

            print("gooogle-----------------------")
            print(e)
            
            return {
                "success": False,
                "error": f"Error al procesar el estudiante: {str(e)}",
                "email": email
            }
    
    def _crear_usuario_en_google(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea un nuevo usuario en Google Workspace
        
        Args:
            validated_data: Datos del usuario a crear
            
        Returns:
            Resultado de la creación
        """
        try:
            # Preparar datos para Google Workspace
            user_data = {
                'primaryEmail': validated_data.get('email'),
                'name': {
                    'givenName': validated_data.get('firstname', 'Usuario'),
                    'familyName': validated_data.get('lastname', 'Nuevo')
                },
                'password': validated_data.get('password', self._generar_password_temporal())
            }
            
            # Crear el usuario
            created_user = self.google_workspace_client.create_user(user_data)
            
            logger.info(f"Usuario {user_data['primaryEmail']} creado exitosamente en Google Workspace")
            
            return {
                "success": True,
                "message": "Usuario creado exitosamente en Google Workspace",
                "email": created_user.get('primaryEmail'),
                "google_id": created_user.get('id'),
                "action": "created"
            }
        
        except Exception as e:
            logger.error(f"Error al crear usuario en Google: {str(e)}")
            return {
                "success": False,
                "error": f"Error al crear usuario en Google Workspace: {str(e)}",
                "email": validated_data.get('email')
            }
    
    def _generar_password_temporal(self) -> str:
        """Genera una contraseña temporal segura"""
        import secrets
        import string
        
        # Generar una contraseña de 16 caracteres con letras, números y símbolos
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(secrets.choice(alphabet) for i in range(16))
        return password