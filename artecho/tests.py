from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Image, UserProfile, Category
from .views import index, download_image, tree_view, user_logout, signup, user_login, add_root, search_results, profile_edit, profile, delete_image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from artecho.forms import LoginForm, SignUpForm, ImageForm, ProfileForm, UserForm
 
# Testing views functionality
class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user)
 
    def test_index_view(self):
        url = reverse('artecho:index')
        request = self.factory.get(url)
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)
 
    def test_download_image_view(self):
        image = Image.objects.create(name='Test Image', file=SimpleUploadedFile("file.jpg", b"file_content"))
        url = reverse('artecho:download_image', kwargs={'slug': image.slug})
        request = self.factory.get(url)
        response = download_image(request, slug=image.slug)
        self.assertEqual(response.status_code, 200)
 
   
 
    def test_profile_edit_view(self):
        url = reverse('artecho:profile_edit', kwargs={'slug': self.user_profile.slug})
        request = self.factory.get(url)
        request.user = self.user
        response = profile_edit(request, slug=self.user_profile.slug)
        self.assertEqual(response.status_code, 200)
 
    def test_profile_view(self):
        url = reverse('artecho:profile', kwargs={'slug': self.user_profile.slug})
        request = self.factory.get(url)
        request.user = self.user
        response = profile(request, slug=self.user_profile.slug)
        self.assertEqual(response.status_code, 200)
 
    def test_delete_image_view(self):
        image = Image.objects.create(name='Test Image', poster=self.user)
        url = reverse('artecho:delete_image', kwargs={'image_id': image.id})
        request = self.factory.post(url)
        request.user = self.user
        response = delete_image(request, image_id=image.id)
        self.assertEqual(response.status_code, 302)
 
# Testing the models functionality
 
class CategoryModelTestCase(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.totalPosts, 0)
        self.assertEqual(category.totalLikes, 0)
        self.assertEqual(category.slug, "test-category")
 
class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
 
    def test_user_profile_creation(self):
        user_profile = UserProfile.objects.create(user=self.user, type="Test Type", bio="Test Bio")
        self.assertEqual(user_profile.user, self.user)
        self.assertEqual(user_profile.type, "Test Type")
        self.assertEqual(user_profile.bio, "Test Bio")
        self.assertEqual(user_profile.totalLikes, 0)
        self.assertEqual(user_profile.slug, "testuser")
 
class ImageModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.category = Category.objects.create(name="Test Category")
 
    def test_image_creation(self):
        image = Image.objects.create(name="Test Image", file="test_image.png", poster=self.user, category=self.category, description="Test Description")
        self.assertEqual(image.name, "Test Image")
        self.assertFalse(image.isAI)
        self.assertEqual(image.file, "test_image.png")
        self.assertIsNone(image.parent)
        self.assertEqual(image.likes, 0)
        self.assertEqual(image.category, self.category)
        self.assertEqual(image.poster, self.user)
        self.assertEqual(image.description, "Test Description")
        self.assertEqual(image.slug, "testuser-test-image")
        self.assertEqual(image.nameSlug, "test-image")
        self.assertEqual(image.slashSlug, "testuser/test-image/")
 
# Testing the forms functionality + some edge cases
 
class LoginFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
 
    def test_login_form(self):
 
        # Valid data
        form_data_valid = {'username': 'testuser', 'password': 'testpassword'}
        form_valid = LoginForm(data=form_data_valid)
        self.assertTrue(form_valid.is_valid())
 
        # Missing username
        form_data_missing_username = {'password': 'testpassword'}
        form_missing_username = LoginForm(data=form_data_missing_username)
        self.assertFalse(form_missing_username.is_valid())
        self.assertIn('username', form_missing_username.errors)
 
class SignUpFormTestCase(TestCase):
    def test_signup_form(self):
        #Valid Data
        form_data_valid = {'username': 'testuser', 'password': 'testpassword', 'password_confirm': 'testpassword'}
        form_valid = SignUpForm(data=form_data_valid)
        self.assertTrue(form_valid.is_valid())
 
        # Missing email
        form_data_missing_email = {'username': 'testuser', 'password': 'testpassword', 'password_confirm': 'testpassword'}
        form_missing_email = SignUpForm(data=form_data_missing_email)
        self.assertTrue(form_missing_email.is_valid())
 
    def test_signup_form_password_mismatch(self):
        # Password mismatch
        form_data_password_mismatch = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword', 'password_confirm': 'mismatchpassword'}
        form_password_mismatch = SignUpForm(data=form_data_password_mismatch)
        self.assertFalse(form_password_mismatch.is_valid())
        self.assertIn('password_confirm', form_password_mismatch.errors)
 
class ImageFormTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
 
    # Incorrect file type
    def test_image_form(self):
        form_data_valid = {
            'name': 'Test Image',
            'isAI': False,
            'category': self.category.id,
            'description': 'Test Description'
        }
        # Create a mock text file (not an image), so it should return fail
        mock_file_content = b'This is a text file'
        mock_file = SimpleUploadedFile('mock_text_file.txt', mock_file_content, content_type='text/plain')
        form_valid = ImageForm(data=form_data_valid, files={'file': mock_file})
 
        self.assertFalse(form_valid.is_valid())
 
        # Missing file
        form_data_missing_file = {
            'name': 'Test Image',
            'isAI': False,
            'category': self.category.id,
            'description': 'Test Description'
        }
        form_missing_file = ImageForm(data=form_data_missing_file)
        self.assertFalse(form_missing_file.is_valid())
        self.assertIn('file', form_missing_file.errors)
 
class ProfileFormTestCase(TestCase):
 
    def test_profile_form(self):
        # Valid data
        form_data_valid = {'bio': 'Test Bio', 'profilePicture': 'test_profile_picture.png'}
        form_valid = ProfileForm(data=form_data_valid)
        self.assertTrue(form_valid.is_valid())
 
        # Missing bio
        form_data_missing_bio = {'profilePicture': 'test_profile_picture.png'}
        form_missing_bio = ProfileForm(data=form_data_missing_bio)
        self.assertFalse(form_missing_bio.is_valid())
        self.assertIn('bio', form_missing_bio.errors)