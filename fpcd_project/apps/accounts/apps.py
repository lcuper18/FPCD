from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = "Cuentas de Usuario"

    def ready(self):
        # Importar signals para crear perfiles automáticamente
        import apps.accounts.signals
