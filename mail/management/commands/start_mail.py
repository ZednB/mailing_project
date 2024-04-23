from django.core.management import BaseCommand

from mail.services import send_mails, list_main


class Command(BaseCommand):

    def handle(self, *args, **options):
        list_main()
