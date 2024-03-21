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


    categories = ["movies", "TV shows", "nature", "Art", "Sports"]

    users = [
        {"username": 'Gary17',
         "email": 'gary17@gmail.com',
         "password": "password1"},
        {"username": 'JoeJ',
         "email": 'Joe89@gmail.com',
         "password": "password7"},
        {"username": 'ogrant22',
         "email": 'ogrant22@gmail.com',
         "password": "webApp7"},
         {"username": 'Angel',
         "email": 'angelina24@gmail.com',
         "password": "October74"},
    ]

    ###adds all the users and categories to the database

    for c in categories:
        u = add_category(c)
        print("added " + u.name)

    for user_data in users:
        u = add_user(user_data["username"],user_data["email"],user_data["password"])
        print("added " + user_data["username"])

    base_images = [
        {"name" : "Darth Vader",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'dart_vader.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Image of the star wars villian",
         "AI": True
        },
        {"name" : "Stranger Things Logo",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'stranger_things_logo.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "TV shows"),
         "desc" : "Logo for the netflix show",
         "AI": False
        },
        {"name" : "Forest",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'forest.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "Clip art of a forest",
         "AI": False
        },
        {"name" : "Landscape",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'landscape.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "JoeJ"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "A painting of a landscape",
         "AI": True
        },
        {"name" : "Metropolis",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'metropolis.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "none"),
         "desc" : "An image of a futuristic city",
         "AI": True
        },
        {"name" : "Grafiti",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'grafiti.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "Angel"),
         "category" : Category.objects.get(name = "Art"),
         "desc" : "An image of a futuristic city",
         "AI": True
        },
        {"name" : "Swimmer",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'swimmer.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "Angel"),
         "category" : Category.objects.get(name = "Sports"),
         "desc" : "An image of a swimmer underwater",
         "AI": True
        },
        {"name" : "Droplet",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'water_drop.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "An image of a water drop splashing",
         "AI": False
        },
        {"name" : "Flower Woman",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'flower_woman.png')),
         "parent" : Image.objects.get(name = "base_root"),
         "poster" : User.objects.get(username = "Angel"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "A woman surrounded by flowers",
         "AI": False
        },
    ]
    
    ### adds 3 images with the "base_root" as their parent to the database

    for image_data in base_images:
        i = add_image(image_data["file"], image_data["name"], image_data["parent"], image_data["poster"], 
                      image_data["desc"], image_data["category"],False)
        print("added " + image_data["name"])

    child_images = [
        {"name" : "Darth Vader (Live action)",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'darth_vader_realistic.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "JoeJ"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "A photo of the live action darth vader",
         "AI": False
        },
        {"name" : "Jim Hopper",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'jim_hopper.png')),
         "parent" : Image.objects.get(slug = "gary17-stranger-things-logo"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "TV shows"),
         "desc" : "One of the protagonists of the show",
         "AI": False
        },
        {"name" : "Tree",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'tree.png')),
         "parent" : Image.objects.get(slug = "ogrant22-forest"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "nature"),
         "desc" : "Clip art of a tree",
         "AI": False
        },
        {"name" : "Coffee splash",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'coffee_splash.png')),
         "parent" : Image.objects.get(slug = "gary17-droplet"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "none"),
         "desc" : "A painting of a coffee cup spilling",
         "AI": False
        },
        {"name" : "Realistic splash",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'realistic_splash.png')),
         "parent" : Image.objects.get(slug = "gary17-droplet"),
         "poster" : User.objects.get(username = "ogrant22"),
         "category" : Category.objects.get(name = "none"),
         "desc" : "A photo of a splash of water",
         "AI": False
        },
        {"name" : "Watercolour splash",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'watercolour_splash.png')),
         "parent" : Image.objects.get(slug = "gary17-droplet"),
         "poster" : User.objects.get(username = "Angel"),
         "category" : Category.objects.get(name = "none"),
         "desc" : "A watercolour painting of a splash of water",
         "AI": False
        },
        {"name" : "Darth Vader vs Jedi",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_vs_jedi.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "JoeJ"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Vader playing handball against a jedi",
         "AI": True
        },
        {"name" : "Darth Vader Baseball",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_baseball.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Vader playing baseball",
         "AI": True
        },
        {"name" : "Darth Vader Fighting",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_fight.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Vader fighting on a starship",
         "AI": True
        },
        #{"name" : "Darth Vader Baseball (Oil)",
        # "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_baseball_oil.png')),
        # "parent" : Image.objects.get(slug = "gary17-darth-vader-baseball"),
        # "poster" : User.objects.get(username = "JoeJ"),
        # "category" : Category.objects.get(name = "movies"),
        # "desc" : "Vader fighting on a starship",
        # "AI": True
        #},
        {"name" : "Darth Vader Water Fountain",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_water_fountain.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "Gary17"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Vader drinking from a water fountain",
         "AI": True
        },
        {"name" : "Darth Vader (Clay)",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_clay.png')),
         "parent" : Image.objects.get(slug = "ogrant22-darth-vader"),
         "poster" : User.objects.get(username = "Angel"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Vader sculpted from clay",
         "AI": True
        },
    ]

    ### adds images which have parents to the database

    for image_data in child_images:
        i = add_image(image_data["file"], image_data["name"], image_data["parent"], image_data["poster"], 
                      image_data["desc"], image_data["category"], image_data["AI"])
        print("added " + image_data["name"])

    

    tier3images = [
        {"name" : "Darth Vader Baseball (Oil)",
         "file" : img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'vader_baseball_oil.png')),
         "parent" : Image.objects.get(slug = "gary17-darth-vader-baseball"),
         "poster" : User.objects.get(username = "JoeJ"),
         "category" : Category.objects.get(name = "movies"),
         "desc" : "Vader fighting on a starship",
         "AI": True
        },
    ]

    for image_data in tier3images:
        i = add_image(image_data["file"], image_data["name"], image_data["parent"], image_data["poster"], 
                      image_data["desc"], image_data["category"], image_data["AI"])
        print("added " + image_data["name"])



def add_user(username, email, password):
    try:
        u = User.objects.get(username = username)
        return u
    except(User.DoesNotExist):
        u = User.objects.get_or_create(username = username, email = email, password = password)[0]
        u.type = "user"
        blank = img.open(os.path.join(os.path.join(settings.STATIC_DIR, 'images'), 'blank_pfp.png'))
        u.profilePicture = convert_to_file(blank, username + "_pfp.png")
        u.save()
        return u
    

def add_image(file, name, parent, poster, desc, category, AI):
    i = Image.objects.get_or_create(name = name, file = convert_to_file(file, name + ".png"), poster = poster, category = category, 
                                    parent = parent, description = desc, isAI = AI)[0]
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
    