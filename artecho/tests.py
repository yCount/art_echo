from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from artecho.models import Category, Image
from populate_script import add_user, add_image, add_category

class PopulateScriptTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(username='tam_rogic18', email='TomRogic@example.com')
        self.user2 = User.objects.create(username='aaron_mooy13', email='AaronMooy@example.com')

        # Create test category
        self.category = Category.objects.create(name='test_category')

    def test_add_user(self):
        # Test adding a user
        user_data = {"username": 'cal_mac42', "forename": 'Cal', "surname": 'Mac', "email": 'CalMac@example.com', "password": "Macdog11"}
        added_user = add_user(**user_data)
        self.assertEqual(added_user.username, user_data["username"])
        self.assertEqual(added_user.email, user_data["email"])

    def test_add_image(self):
        # Test adding an image
        image_data = {"name" : "Test Image", "file" : "test_file.png", "parent" : None, "poster" : self.user1, "desc" : "Test description", "category" : self.category}
        added_image = add_image(**image_data)
        self.assertEqual(added_image.name, image_data["name"])
        self.assertEqual(added_image.poster, image_data["poster"])

    def test_add_category(self):
        # Test adding a category
        category_name = "Test Category"
        added_category = add_category(category_name)
        self.assertEqual(added_category.name, category_name)

    def test_add_user_already_exists(self):
        # Test adding a user that already exists
        user_data = {"username": 'cal_mac42', "forename": 'Cal, "surname": 'Mac', "email": 'CalMac@example.com', "password": "Macdog11"}
        added_user = add_user(**user_data)
        self.assertEqual(added_user, self.user1)

    def test_add_image_with_parent(self):
        # Test adding an image with a parent
        parent_image = Image.objects.create(name='Parent Image', poster=self.user1, category=self.category)
        image_data = {"name": "Child Image", "file": "test_file.png", "parent": parent_image, "poster": self.user2, "desc": "Test description", "category": self.category}
        added_image = add_image(**image_data)
        self.assertEqual(added_image.parent, parent_image)

    def test_add_category_duplicate(self):
        # Test adding a category with duplicate name
        category_name = "Test Category"
        added_category1 = add_category(category_name)
        added_category2 = add_category(category_name)
        self.assertNotEqual(added_category1, added_category2)

    def test_add_image_without_category(self):
        # Test adding an image without category
        image_data = {"name": "No Category Image", "file": "test_file.png", "parent": None, "poster": self.user1, "desc": "Test description", "category": None}
        with self.assertRaises(ValueError):
            added_image = add_image(**image_data)

    def test_add_user_no_profile_picture(self):
        # Test adding a user without profile picture
        user_data = {"username": 'JotaJota', "forename": 'Joao', "surname": 'Felipe', "email": 'Jota@example.com', "password": "OnTheWing17"}
        added_user = add_user(**user_data)
        self.assertTrue(added_user.profilePicture)

    def test_add_image_invalid_parent(self):
        # Test adding an image with invalid parent
        parent_image = Image.objects.create(name='Invalid Parent Image', poster=self.user1, category=self.category)
        invalid_parent = Image.objects.create(name='Invalid Image', poster=self.user1, category=self.category)
        image_data = {"name": "Child Image", "file": "test_file.png", "parent": invalid_parent, "poster": self.user2, "desc": "Test description", "category": self.category}
        with self.assertRaises(ValueError):
            added_image = add_image(**image_data)

    def test_add_category_no_name(self):
        # Test adding a category without a name
        with self.assertRaises(ValueError):
            added_category = add_category(None)
