import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art_echo.settings')

import django
django.setup()
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files import File

from artecho.models import Category, Image, User
from art_echo import settings

from PIL import Image as img
import io
import sys 
from tempfile import TemporaryFile

###### INPROGRESS

def populate():
    users = [
        {"username": 'Gary17',
         "forename": 'Gary',
         "surname": 'Smith',
         "email": 'gary17@gmail.com',
         "password": "password1"},
        {"username": 'JoeJ',
         "forename": 'Joe',
         "surname": 'Johnson',
         "email": 'Joe89@gmail.com',
         "password": "password7"},
        {"username": 'ogrant22',
         "forename": 'Oran',
         "surname": 'Grant',
         "email": 'ogrant22@gmail.com',
         "password": "webApp7"},
    ]


    c = Category.objects.get_or_create(name = "none", slug = "none")[0]
    c.save()
    ###creates a base root for all other trees to build off of
    try:
        Image.objects.get(name = "base_root")
    except(Image.DoesNotExist):
        base_image = img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'base_root.png'))
        i = Image.objects.get_or_create(name = "base_root", isAI = False, file = convert_to_file(base_image, "base_root.png"), parent = None,
                                    category = c, poster = None, description = "The base root")[0]
        i.save()

    for user_data in users:
        u = add_user(user_data["username"],user_data["email"],user_data["forename"],user_data["surname"],user_data["password"])
        print("added " + user_data["username"])




def add_user(username, fore, sur, email, password):
    try:
        u = User.objects.get(username = username)
        return u
    except(User.DoesNotExist):
        u = User.objects.get_or_create(username = username, email = email, forename = fore, surname = sur, password = password)[0]
        u.type = "user"
        blank = img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'blank_pfp.png'))
        u.profilePicture = convert_to_file(blank, username + "_pfp.png")
        u.save()
        return u

def convert_to_file(image, name): ##function to convert PIL image to an uploadable file with a name
    output = io.BytesIO()
    image.save(output, format='PNG', quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', name, 'image/png', sys.getsizeof(output), None)
    
if __name__ == '__main__':
    print('Starting ArtEcho population script...')
    populate()
    print("population complete")
    