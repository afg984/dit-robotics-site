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

    LEVEL_NAMES = ('UNVERIFIED', 'USER', 'MEMBER', 'OPERATOR', 'ADMIN')
    LEVEL_CSS = ('muted', 'normal', 'success', 'warning', 'danger')
    TOKEN_LENGTH = 64
    user = models.OneToOneField(User, primary_key=True)
    objects = ProfileManager()

    @property
    def is_member(self):
        return KnownMemberEmail.objects.filter(email=self.user.email).exists()

    @property
    def access_level(self):
        if self.user.is_superuser:
            return 4
        elif self.user.is_staff:
            return 3
        elif self.is_member:
            return 2
        else:
            return 1

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

    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def __str__(self):
        return self.user.username


class KnownMemberEmail(models.Model):
    email = models.EmailField(unique=True)
