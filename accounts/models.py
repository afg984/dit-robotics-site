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


class ProfileManager(models.Manager):
    def create_user(self, username, password, email):
        return self.create(
            user=User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
        )


class Profile(models.Model):
    class Meta:
        permissions = (
            ('inactive_user', 'Can mark a user as active = False'),
            ('remove_user', 'Can delete another user'),
            ('view_email', "Can view other's email"),
            ('view_last_login', "Can view other's login time"),
        )

    LEVEL_NAMES = ('NOEMAIL', 'USER', 'MEMBER', 'MOD', 'ADMIN')
    LEVEL_CSS = ('muted', 'normal', 'success', 'warning', 'danger')
    TOKEN_LENGTH = 64
    user = models.OneToOneField(User, primary_key=True)
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=TOKEN_LENGTH, default="")
    email_token_expire = models.DateTimeField(null=True)
    objects = ProfileManager()

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
            '<a href="{href}">{username}</a>',
            href=self.get_absolute_url(),
            username = self.user.get_username(),
        )

    def set_email(self, email):
        self.user.email = email
        self.email_verified = False
        self.user.save()
        self.save()

    def set_email_verified(self):
        self.email_verified = True
        self.email_token = ''
        self.email_token_expire = None
        self.save()

    def get_email_token(self):
        if not self.email_token_alive:
            token = gen_token(self.TOKEN_LENGTH)
            if not Profile.objects.filter(email_token=token).exists():
                token = gen_token(self.TOKEN_LENGTH)
            self.email_token = token
            self.save()
        return self.email_token

    @property
    def email_token_alive(self):
        if self.email_token_expire is None:
            return False
        return len(self.email_token) == self.TOKEN_LENGTH and self.email_token_expire > timezone.now()

    def refresh_email_token(self, delay=timezone.timedelta(minutes=30)):
        self.email_token_expire = timezone.now() + delay
        self.save()

    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def __str__(self):
        return self.user.username


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
