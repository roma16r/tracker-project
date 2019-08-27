from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from PIL import Image
from django.conf import settings
from django.contrib.auth.models import Group


class User(AbstractUser):
    email = models.EmailField('email address', blank=False, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=60, blank=True)
    image = models.ImageField(upload_to='avatars', blank=True)
    groups = models.ManyToManyField(Group)

    class Meta:
        permissions = [
            ('view_user_list', 'Can view user list')
        ]

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 200 or img.width > 200:
                size = (200, 200)
                img.thumbnail(size)
                img.save(self.image.path)

    def image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + 'core/img/avatars/default.png'

