from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='ogrant22', 
            email='test@example.com', 
            type='test', 
            profilePicture='path/to/image.jpg', 
            bio='test bio', 
            forename='Oran', 
            surname='Grant', 
            password='testpassword'
        )

    def test_slug_creation(self):
        self.assertEqual(self.user.slug, 'ogrant22')