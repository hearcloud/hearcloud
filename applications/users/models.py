from __future__ import unicode_literals

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from django.template.defaultfilters import slugify

from easy_thumbnails.fields import ThumbnailerImageField


class UserManager(BaseUserManager, models.Manager):
    """
    Represents our custom user model manager
    """

    def _create_user(self, username, email, password, is_staff, is_superuser,
                     **extra_fields):
        """
        Base method to create the custom users
        """
        email = self.normalize_email(email)  # To lowercase
        if not email:
            raise ValueError('El email debe ser obligatorio')

        user = self.model(username=username, email=email, is_active=True,
                          is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Represents the users models.
    """

    def get_full_name(self):
        return self.username

    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    picture = ThumbnailerImageField(upload_to='profile_images', blank=True)

    slug = models.SlugField(unique=True)

    objects = UserManager()  # objects is the manager of every model (users.objects.all(), ...)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return self.username

    def get_songs_count(self):
        return self.song_set.all().count()

    def __unicode__(self):
        return self.username
