from django.core.management.base import BaseCommand
from core_apps.mq_manager.mq_callback import main


class Command(BaseCommand):
    '''Consumes Messages from Code Submission Queue 
       Published by Code Manager Service.
    '''
    help = "Consumes messages from RabbitMQ Code Submission Queue"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("Consuming messages from Code Submission Queue...")
        )
        main()
