from typing import Any, Dict
import logging

from course_sync_service.app.core.integrations.google_workspace.google_workspace_users import GoogleWorkspaceUsers

logger = logging.getLogger(__name__)


class CrearEstudiante:
    def __init__(self, google_workspace_client: GoogleWorkspaceUsers):
        print(f"[DEBUG] Inicializando CrearEstudiante")
        print(f"[DEBUG] Tipo de google_workspace_client: {type(google_workspace_client)}")
        print(f"[DEBUG] Credenciales del cliente: {type(google_workspace_client.credentials)}")
        print(f"[DEBUG] Service account email: {getattr(google_workspace_client.credentials, 'service_account_email', 'N/A')}")
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
        print(f"\n{'='*60}")
        print(f"[DEBUG] Iniciando ejecutar()")
        print(f"[DEBUG] validated_data completo: {validated_data}")
        logger.info(f"Iniciando creación/verificación de estudiante: {validated_data}")
        
        # Validar que el email esté presente
        try:
            email = validated_data["users"][0]["email"]
            print(f"[DEBUG] Email extraído: {email}")
        except (KeyError, IndexError, TypeError) as e:
            print(f"[DEBUG ERROR] Error al extraer email: {e}")
            print(f"[DEBUG ERROR] Estructura de validated_data: {type(validated_data)}")
            return {
                "success": False,
                "error": f"Error al extraer email de los datos: {str(e)}"
            }
        
        if not email:
            print(f"[DEBUG] Email está vacío")
            return {
                "success": False,
                "error": "El campo 'email' es requerido"
            }
        
        try:
            print(f"[DEBUG] Verificando si usuario existe en Google Workspace...")
            print(f"[DEBUG] Credenciales válidas: {hasattr(self.google_workspace_client.credentials, 'valid')}")
            print(f"[DEBUG] Credenciales expiradas: {getattr(self.google_workspace_client.credentials, 'expired', 'N/A')}")
            
            # Verificar si el usuario existe en Google Workspace
            user_exists = self.google_workspace_client.user_exists(email)
            
            print(f"[DEBUG] Resultado de user_exists: {user_exists}")
            print(f"{'='*60}\n")
            
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
                print(f"[DEBUG] Usuario {email} NO existe en Google Workspace")
                
                # Opción 1: Solo verificar (comportamiento actual)
                return {
                    "success": False,
                    "error": "El usuario no existe en Google Workspace",
                    "email": email
                }
                
                # Opción 2: Crear el usuario automáticamente (descomenta si deseas esto)
                # return self._crear_usuario_en_google(validated_data)
        
        except Exception as e:
            print(f"\n[DEBUG ERROR] {'='*60}")
            print(f"[DEBUG ERROR] Excepción capturada: {type(e).__name__}")
            print(f"[DEBUG ERROR] Mensaje: {str(e)}")
            print(f"[DEBUG ERROR] Email: {email}")
            
            import traceback
            print(f"[DEBUG ERROR] Traceback completo:")
            print(traceback.format_exc())
            print(f"[DEBUG ERROR] {'='*60}\n")
            
            logger.error(f"Error al verificar/crear estudiante {email}: {str(e)}")
            
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
        print(f"[DEBUG] Iniciando _crear_usuario_en_google()")
        print(f"[DEBUG] validated_data: {validated_data}")
        
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
            
            print(f"[DEBUG] user_data preparado: {user_data}")
            
            # Crear el usuario
            created_user = self.google_workspace_client.create_user(user_data)
            
            print(f"[DEBUG] Usuario creado exitosamente: {created_user}")
            logger.info(f"Usuario {user_data['primaryEmail']} creado exitosamente en Google Workspace")
            
            return {
                "success": True,
                "message": "Usuario creado exitosamente en Google Workspace",
                "email": created_user.get('primaryEmail'),
                "google_id": created_user.get('id'),
                "action": "created"
            }
        
        except Exception as e:
            print(f"[DEBUG ERROR] Error al crear usuario: {str(e)}")
            import traceback
            print(f"[DEBUG ERROR] Traceback: {traceback.format_exc()}")
            
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
        
        print(f"[DEBUG] Generando password temporal")
        
        # Generar una contraseña de 16 caracteres con letras, números y símbolos
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = ''.join(secrets.choice(alphabet) for i in range(16))
        
        print(f"[DEBUG] Password generado (longitud: {len(password)})")
        
        return password