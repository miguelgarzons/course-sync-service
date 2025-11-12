class SQLServerRouter:
    """
    Router para dirigir las operaciones de lectura hacia SQL Server
    para modelos no gestionados (managed=False).
    """

    def db_for_read(self, model, **hints):
        if not model._meta.managed:
            return "sqlserver"
        return None

    def db_for_write(self, model, **hints):
        # Evitamos escrituras en SQL Server (solo lectura)
        if not model._meta.managed:
            return None
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Evita migraciones hacia SQL Server
        if db == "sqlserver":
            return False
        return True
