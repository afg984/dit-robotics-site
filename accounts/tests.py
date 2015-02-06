from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from accounts.models import Profile
# Create your tests here.

class AccountTestCase(TestCase):
    def setUp(self):
        self.username = 'account_test_user'
        self.password = 'account_test_password'
        self.email = 'account_test_email@example.com'
        self.registration_response = self.client.post(
            reverse('registration'),
            {
                'username': self.username,
                'password1': self.password,
                'password2': self.password,
                'email': self.email,
            },
        )
        self.user = User.objects.get(username=self.username)

    def test_redirect_registered_account_to_profile_page(self):
        self.assertRedirects(self.registration_response, reverse('profile'))

    def test_user_has_correct_email(self):
        self.assertEqual(
            self.user.email,
            self.email
        )

    def test_user_has_profile(self):
        self.user.profile
    
    def test_user_email_is_not_verified(self):
        self.assertFalse(self.user.profile.email_verified)

    def test_user_is_noemail(self):
        self.assertEqual(self.user.profile.level_name, 'NOEMAIL')

    def test_user_can_login(self):
        response = self.client.post(
            reverse('login'),
            {
                'id_username': self.username,
                'id_password': self.password,
            },
            follow=True
        )
        self.assertContains(response, self.username)
        self.assertContains(response, 'Log out')
    

class ProfileManagerTest(TestCase):
    def setUp(self):
        self.username = 'testuser123'
        self.password = 'testpassword1234'
        self.email = 'email123@test.com'
        self.profile = Profile.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_profile_manager_can_create_user(self):
        user = User.objects.get(username=self.username)
        self.assertEqual(self.profile, user.profile)
