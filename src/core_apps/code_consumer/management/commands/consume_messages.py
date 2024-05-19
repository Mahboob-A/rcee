from django.core.management.base import BaseCommand
from core_apps.code_consumer.mq_callback import main


class Command(BaseCommand):
    help = "Consumes messages from RabbitMQ"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Consuming messages from RabbitMQ..."))
        main()
