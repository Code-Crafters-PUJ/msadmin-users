from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Account"

    def ready(self):
        from Account.rabbitmq import create_jwt_validation_queue
        create_jwt_validation_queue()
        from .processrabbitmq import process_jwt_validation_requests
        process_jwt_validation_requests()
