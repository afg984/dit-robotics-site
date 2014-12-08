from django.test import TestCase, Client


class SiteSimpleTestCase(TestCase):
    def test_home_response_starts_with_doctype_html(self):
        client = Client()
        response = client.get('')
        assertion = b'<!DOCTYPE html>'
        self.assertSequenceEqual(
            response.content[:len(assertion)],
            assertion,
            'response content should start with %r' % assertion,
        )
