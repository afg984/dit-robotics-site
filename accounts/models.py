from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.utils import timezone

from .tokens import gen_token

def get_profile(user):
    try:
        return user.profile
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)

# Create your models here.
class Profile(models.Model):
    LEVEL_NAMES = ('NOEMAIL', 'USER', 'MEMBER', 'MOD', 'ADMIN')
    LEVEL_CSS = ('muted', 'normal', 'success', 'warning', 'danger')
    TOKEN_LENGTH = 64
    user = models.OneToOneField(User)
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=TOKEN_LENGTH, default="")
    email_token_expire = models.DateTimeField(null=True)

    @property
    def is_member(self):
        return KnownMemberEmail.objects.filter(email=self.user.email).exists()

    @property
    def access_level(self):
        if self.user.is_superuser:
            return 4
        elif False: # group moderator not implemented yet
            return 3
        elif self.email_verified:
            if self.is_member:
                return 2
            else:
                return 1
        else:
            return 0

    @property
    def level_name(self):
        return self.LEVEL_NAMES[self.access_level]

    @property
    def level_css(self):
        return self.LEVEL_CSS[self.access_level]

    @property
    def html_link(self):
        return format_html(
            '<a class="{class_}" href="{href}">{username}</a>',
            class_="text-" + self.level_css,
            href=reverse('profile', args=[self.user.username]),
            username = self.user.get_username(),
        )

    def set_email(self, email):
        self.user.email = email
        self.email_verified = False
        self.user.save()
        self.save()

    def gen_email_token(self):
        token = gen_token(self.TOKEN_LENGTH)
        self.email_token = token
        self.email_token_expire = timezone.now() + timezone.timedelta(minutes=30)
        self.save()
        return token


class KnownMemberEmail(models.Model):
    email = models.EmailField(unique=True)

    @classmethod
    def load_csv(cls, path):
        import csv
        with open(path, newline='') as file:
            reader = csv.reader(file)

            first = next(reader)
            index = first.index('電子郵件')

            for row in reader:
                email = row[index].strip()
                obj, created = cls.objects.get_or_create(email=email)
                if created:
                    print('Added', email, 'to', cls.__name__)
