from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from accounts.models import Profile
# Create your tests here.

class AccountRegistrationTestCase(TestCase):
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
        self.assertRedirects(
            self.registration_response,
            reverse('profile', args=[self.user.username])
        )

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


class UserSetupTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser123'
        self.password = 'testpassword1234'
        self.email = 'email123@example.com'
        self.profile = Profile.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )


class ProfileManagerTest(UserSetupTestCase):
    def test_profile_manager_can_create_user(self):
        user = User.objects.get(username=self.username)
        self.assertEqual(self.profile, user.profile)


class ProfileViewTest(UserSetupTestCase):
    def test_profile_index_is_404(self):
        response = self.client.get('/profile/')
        self.assertEqual(404, response.status_code)

    def test_get_absolute_url_implemented(self):
        self.assertIn('profile', self.profile.get_absolute_url())

    def test_get_absolute_url_points_to_profile_page(self):
        response = self.client.get(self.profile.get_absolute_url())
        self.assertContains(response, self.username)
        self.assertContains(response, 'Profile')

    def test_profile_view_content(self):
        response = self.client.get(self.profile.get_absolute_url())
        self.assertEqual(200, response.status_code)
        self.assertContains(response, self.username)
        self.assertNotContains(response, self.password)
        self.assertNotContains(response, self.email)

    def test_login_redirects_to_profile(self):
        response = self.client.post(
            reverse('login'),
            dict(
                username=self.username,
                password=self.password,
            ),
            follow=True,
        )
        self.assertRedirects(response, self.profile.get_absolute_url())
