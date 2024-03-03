import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'art_echo.settings')

import django
django.setup()
from django.core.files.uploadedfile import InMemoryUploadedFile

from artecho.models import Category, Image, User
from art_echo import settings

from PIL import Image
import io
import sys 

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

    for user_data in users:
        u = add_user(user_data["username"],user_data["email"],user_data["forename"],user_data["surname"],user_data["password"])
        print("added " + user_data["username"])




def add_user(username, fore, sur, email, password):
    u = User.objects.get_or_create(username = username, email = email, forename = fore, surname = sur, password = password)[0]
    u.type = "user"
    blank = Image.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'blank_pfp.png'))
    u.profilePicture = convert_to_pfp(blank)
    u.save()
    return u

def convert_to_pfp(image): ##function to convert PIL image to an uploadable file of a set size
    image = image.convert('RGB')
    image = image.resize((800, 800))
    output = io.BytesIO()
    image.save(output, format='PNG', quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', "profilePic", 'image/jpeg', sys.getsizeof(output), None)
    
if __name__ == '__main__':
    print('Starting ArtEcho population script...')
    populate()
    print("population complete")
    