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
import glob



def populate():

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


    categories = ["movies", "TV shows", "nature"]

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

    ###adds all the users and categories to the database

    for c in categories:
        u = add_category(c)
        print("added " + u.name)

    for user_data in users:
        u = add_user(user_data["username"],user_data["email"],user_data["forename"],user_data["surname"],user_data["password"])
        print("added " + user_data["username"])

    base_images = [
        {"name" : "Darth Vader",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'dart_vader.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Image of the star wars villian",
        },
        {"name" : "Stranger Things Logo",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'stranger_things_logo.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "TV shows"),
         "desc" : "Logo for the netflix show",
        },
        {"name" : "Forest",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'forest.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "Clip art of a forest",
        }
    ]
    
    ### adds 3 images with the "base_root" as their parent to the database

    for image_data in base_images:
        i = add_image(image_data["file"], image_data["name"], image_data["parent"], image_data["poster"], 
                      image_data["desc"], image_data["category"])
        print("added " + image_data["name"])

    child_images = [
        {"name" : "Darth Vader (Live action)",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'darth_vader_realistic.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "JoeJ"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "A photo of the live action darth vader",
        },
        {"name" : "Jim Hopper",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'jim_hopper.png')),
         "parent" : Image.objects.get(slug = "gary17-stranger-things-logo"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "TV shows"),
         "desc" : "One of the protagonists of the show",
        },
        {"name" : "Tree",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'tree.png')),
         "parent" : Image.objects.get(slug = "ogrant22-forest"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "Clip art of a tree",
        }
    ]

    ### adds 3 images which have parents to the database

    for image_data in child_images:
        i = add_image(image_data["file"], image_data["name"], image_data["parent"], image_data["poster"], 
                      image_data["desc"], image_data["category"])
        print("added " + image_data["name"])



def add_user(username, email, forename, surname, password):
    user, created = User.objects.get_or_create(username=username, defaults={
        "email": email,
        "first_name": forename,
        "last_name": surname,
    })
    if created:
        user.set_password(password)
        user.save()
    return user
    

def add_image(file, name, parent, poster, desc, category):
    i = Image.objects.get_or_create(name = name, file = convert_to_file(file, name + ".png"), poster = poster, category = category, 
                                    parent = parent, description = desc, isAI = False)[0]
    i.save()
    return i


def add_category(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    return c
    

def convert_to_file(image, name): ##function to convert PIL image to an uploadable file with a name
    output = io.BytesIO()
    image.save(output, format='PNG', quality=85)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', name, 'image/png', sys.getsizeof(output), None)
    
if __name__ == '__main__':
    print('Starting ArtEcho population script...')
    #clears previous contents of database
    Image.objects.all().delete()
    User.objects.all().delete()
    Category.objects.all().delete()
    imageFiles = glob.glob(os.path.join(settings.MEDIA_DIR, 'images') + "/*.png")
    for file in imageFiles:
        os.remove(file)
    pfpFiles = glob.glob(os.path.join(settings.MEDIA_DIR, 'profilePics') + "/*.png")
    for file in pfpFiles:
        os.remove(file)



    populate()
    print("population complete")
    