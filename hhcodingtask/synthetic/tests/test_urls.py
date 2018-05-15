from django.urls import reverse, resolve

from test_plus.test import TestCase


class TestSyntheticURLs(TestCase):
    """Test URL patterns for users app."""

    def test_list_reverse(self):
        self.assertEqual(reverse("synthetic:list"), "/synthetic/")

    def test_update_reverse(self):
        self.assertEqual(reverse("synthetic:detail", kwargs={'pk': 8}), "/synthetic/detail/8/")
