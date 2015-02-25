import os
from optparse import make_option
from ._py35glob import glob

from django.core.management.base import BaseCommand, CommandError

from drs.settings import BASE_DIR, MEDIA_ROOT
from drive.models import DriveFile

class Command(BaseCommand):
    help = 'cleanup drive files'

    option_list = BaseCommand.option_list + (
        make_option(
            '--noinput',
            action='store_true',
            dest='noinput',
            default=False,
            help='do not prompt',
        ),
    )

    def format_info(self, name, value):
        self.stdout.write(
            '{}  {}'.format(
                name,
                len(value)
            )
        )

    def handle(self, *, noinput, **options):
        filesystem = glob(os.path.join(BASE_DIR, MEDIA_ROOT, '**'), recursive=True)
        database = [file.file.path for file in DriveFile.objects.all()]
        filesystem = set(filter(os.path.isfile, filesystem))
        database = set(database)
        to_delete = filesystem - database
        errors = database - filesystem
        for path in sorted(to_delete):
            self.stdout.write('[-] %s' % path)
        for path in sorted(errors):
            self.stdout.write('[*] %s' % path)
        self.stdout.write('=' * 79)
        self.stdout.write('Summary:')
        self.format_info('      DATABASE', database)
        self.format_info('    FILESYSTEM', filesystem)
        self.format_info('[-]  TO DELETE', to_delete)
        self.format_info('[*]     ERRORS', errors)
        if not noinput and input('Do you wish to continue? [y/N] ').lower() != 'y':
            raise CommandError('Aborted')
        for path in to_delete:
            os.remove(path)
        print('Files deleted.')
