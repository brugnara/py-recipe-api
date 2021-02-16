import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """command"""

    def handle(self, *args, **options):
        self.stdout.write('loading...')
        db_conn = None

        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('DB ko, wait')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('OK!'))
