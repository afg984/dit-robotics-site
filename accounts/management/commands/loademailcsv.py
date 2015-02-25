import csv
from optparse import make_option

from django.core.management.base import BaseCommand

from accounts.models import KnownMemberEmail


class Command(BaseCommand):
    args = '<filename.csv>'
    help = 'load email from csv file'

    option_list = BaseCommand.option_list + (
        make_option(
            '--append',
            action='store_true',
            dest='append',
            default=False,
            help='Append new emails instead of rewrite',
        ),
    )

    def handle(self, filename, *, append, **options):
        emails = self.get_emails_from_csv(filename)
        add_count = 0
        if append:
            deletion = KnownMemberEmail.objects.none()
        else:
            deletion = KnownMemberEmail.objects.exclude(
                email__in=emails
            )
        del_count = deletion.count()
        for deltarget in deletion:
            self.stdout.write('- %s' % deltarget.email)
            deltarget.delete()
        for email in emails:
            obj, created = KnownMemberEmail.objects.get_or_create(email=email)
            if created:
                self.stdout.write('+ %s' % email)
                add_count += 1
        self.stdout.write('{} deleted, {} added.'.format(del_count, add_count))

    def get_emails_from_csv(self, path):
        with open(path, newline='\n') as file:
            reader = csv.reader(file)

            first = next(reader)
            index = first.index('電子郵件')

            return [row[index].strip() for row in reader]
