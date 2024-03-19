from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser

# Create your models here.
 
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
        return self.slug


class User(AbstractUser):
    type = models.CharField(max_length=128, null=False)
    profilePicture = models.ImageField(null=False, upload_to='profilePics/', default='images/blank_pfp.png')
    bio = models.TextField(max_length=1000)
    totalLikes = models.IntegerField(default=0)
    liked = models.ManyToManyField('Image', default=None)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'users'

    def __str__(self):
        return self.slug

class Image(models.Model):
    name = models.CharField(max_length=128, null = False)
    isAI = models.BooleanField(default = False)
    file = models.ImageField(null = False, upload_to= 'images/')
    parent = models.ForeignKey('Image', on_delete=models.DO_NOTHING, null = True) ###unsure if this is the correct delete mode
    likes = models.IntegerField(default = 0)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)
    poster = models.ForeignKey('User', on_delete=models.DO_NOTHING, null = True)
    description = models.TextField(max_length=1000, unique=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if self.poster == None:
            full_slug = self.name
        else:
            full_slug = str(self.poster) + "-" + self.name
        self.slug = slugify(full_slug) #Image slug is a concatenation of the user who posted it and the name
        super(Image, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'images'

    def __str__(self):
        return self.slug