import os

from django.core import management
from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    help = 'Syncdb and create admin user'

    def handle_noargs(self, **options):
        try:
            os.remove(settings.DATABASES['default']['NAME'])
        except OSError:
            pass
        management.call_command('syncdb', interactive=False)
        management.call_command('createsuperuser', username='admin', email='admin@host.local')

        fixture_dir = settings.FIXTURE_DIRS[0]

        management.call_command('loaddata', fixture_dir + "website_test")
        self.stdout.write('Successfully initialized')

