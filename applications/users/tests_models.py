from django.test import TestCase
from .models import User

# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
                username = 'testuser',
                email = 'testuser@testdomain.com',
                password = 'testpassword',
        )
        self.superuser = User.objects.create_superuser(
                username = 'admin',
                email = 'admin@testdomain.com',
                password = 'adminpassword',
        )

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'testuser')

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), 'testuser')

    def test_get_songs_count(self):
        self.assertEqual(self.user.get_songs_count(), 0)

    def test__unicode__(self):
        self.assertEqual(self.user.__unicode__(), 'testuser')

    def test_save(self):
        self.assertEqual(self.user.slug, 'testuser')  # Slug
