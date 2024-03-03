from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.

##admin details
#username = admin1
#password = ArtEcho1
 
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, null = False)
    totalPosts = models.IntegerField(default = 0)
    totalLikes = models.IntegerField(default = 0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
class User(models.Model):
    username = models.CharField(max_length=128, unique=True, null = False)
    email = models.EmailField(null = False)
    type = models.CharField(max_length=128, null = False)
    profilePicture = models.ImageField(null = False, upload_to= 'profilePics/')  ##directory where profile pics will be stored
    bio = models.TextField(max_length=1000)
    forename = models.CharField(max_length=128, null = False)
    surname = models.CharField(max_length=128, null = False)
    totalLikes = models.IntegerField(default = 0)
    liked = models.ManyToManyField('Image')
    password = models.CharField(max_length=128, null = False)  ###will be encrypted when taken in via a form "(widget=forms.PasswordInput()"
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username

class Image(models.Model):
    name = models.CharField(max_length=128, unique=True, null = False)
    isAI = models.BooleanField()
    file = models.ImageField(null = False)
    parent = models.ForeignKey('Image', on_delete=models.PROTECT, null = True) ###unsure if this is the correct delete mode
    likes = models.IntegerField(default = 0)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, null = False)
    poster = models.ForeignKey('User', on_delete=models.PROTECT, null = False)
    description = models.TextField(max_length=1000, unique=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Image, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'images'

    def __str__(self):
        return self.name
    