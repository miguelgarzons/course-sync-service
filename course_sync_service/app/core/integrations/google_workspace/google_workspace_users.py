from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleWorkspaceUsers:
    def __init__(self, credentials: Credentials):
        self.credentials = credentials
        self._ensure_valid_credentials()
        self.service = build('admin', 'directory_v1', credentials=self.credentials)

    def _ensure_valid_credentials(self):
        """Asegura que las credenciales sean válidas, refrescándolas si es necesario"""
        if not self.credentials.valid:
            if self.credentials.expired and self.credentials.refresh_token:
                try:
                    self.credentials.refresh(Request())
                except Exception as e:
                    raise Exception(f"Error al refrescar credenciales de Google: {str(e)}")
            else:
                raise Exception("Las credenciales de Google no son válidas y no se pueden refrescar")

    def user_exists(self, email: str) -> bool:
        """
        Verifica si un usuario existe en Google Workspace
        
        Args:
            email: Email del usuario a verificar
            
        Returns:
            True si el usuario existe, False si no existe
            
        Raises:
            Exception: Si hay un error diferente a 404 (usuario no encontrado)
        """
        if not email:
            raise ValueError("El email no puede estar vacío")
        
        try:
            # Refrescar credenciales antes de cada llamada si es necesario
            self._ensure_valid_credentials()
            
            # Intentar obtener el usuario
            self.service.users().get(userKey=email).execute()
            return True
            
        except HttpError as e:
            if e.resp.status == 404:
                # Usuario no encontrado
                return False
            elif e.resp.status == 403:
                raise Exception(f"Acceso denegado. Verifica que la cuenta de servicio tenga permisos de Admin SDK: {str(e)}")
            else:
                raise Exception(f"Error al verificar usuario en Google Workspace: {str(e)}")
        except Exception as e:
            raise Exception(f"Error inesperado al verificar usuario: {str(e)}")

    def get_user(self, email: str):
        """
        Obtiene los datos completos de un usuario de Google Workspace
        
        Args:
            email: Email del usuario
            
        Returns:
            Diccionario con los datos del usuario o None si no existe
        """
        if not email:
            raise ValueError("El email no puede estar vacío")
        
        try:
            self._ensure_valid_credentials()
            user = self.service.users().get(userKey=email).execute()
            return user
        except HttpError as e:
            if e.resp.status == 404:
                return None
            raise Exception(f"Error al obtener usuario: {str(e)}")

    def create_user(self, user_data: dict):
        """
        Crea un nuevo usuario en Google Workspace
        
        Args:
            user_data: Diccionario con los datos del usuario
                Ejemplo:
                {
                    'primaryEmail': 'usuario@dominio.com',
                    'name': {
                        'givenName': 'Juan',
                        'familyName': 'Pérez'
                    },
                    'password': 'ContraseñaSegura123!'
                }
        
        Returns:
            Diccionario con los datos del usuario creado
        """
        try:
            self._ensure_valid_credentials()
            user = self.service.users().insert(body=user_data).execute()
            return user
        except HttpError as e:
            raise Exception(f"Error al crear usuario en Google Workspace: {str(e)}")

    def list_users(self, domain: str = None, max_results: int = 100):
        """
        Lista usuarios de Google Workspace
        
        Args:
            domain: Dominio para filtrar usuarios (opcional)
            max_results: Número máximo de resultados (default: 100)
            
        Returns:
            Lista de usuarios
        """
        try:
            self._ensure_valid_credentials()
            results = self.service.users().list(
                customer='my_customer',
                maxResults=max_results,
                orderBy='email',
                domain=domain
            ).execute()
            return results.get('users', [])
        except HttpError as e:
            raise Exception(f"Error al listar usuarios: {str(e)}")

    def update_user(self, email: str, user_data: dict):
        """
        Actualiza los datos de un usuario existente
        
        Args:
            email: Email del usuario a actualizar
            user_data: Diccionario con los campos a actualizar
            
        Returns:
            Diccionario con los datos del usuario actualizado
        """
        try:
            self._ensure_valid_credentials()
            user = self.service.users().update(
                userKey=email,
                body=user_data
            ).execute()
            return user
        except HttpError as e:
            raise Exception(f"Error al actualizar usuario: {str(e)}")

    def delete_user(self, email: str):
        """
        Elimina un usuario de Google Workspace
        
        Args:
            email: Email del usuario a eliminar
        """
        try:
            self._ensure_valid_credentials()
            self.service.users().delete(userKey=email).execute()
            return True
        except HttpError as e:
            raise Exception(f"Error al eliminar usuario: {str(e)}")