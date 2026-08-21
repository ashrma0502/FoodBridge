from django.apps import AppConfig


class DispatchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dispatch"
    verbose_name = "Dispatch"

    def ready(self):
        """Validate that OR-Tools is importable at startup."""
        try:
            from ortools.constraint_solver import routing_enums_pb2  # noqa: F401
            from ortools.constraint_solver import pywraprp  # noqa: F401
        except ImportError:
            # Soft warning — don't crash the server; just log it
            import warnings
            warnings.warn(
                "OR-Tools is not installed. Dispatch route optimisation will not work. "
                "Install it with: pip install ortools",
                ImportWarning,
                stacklevel=2,
            )
