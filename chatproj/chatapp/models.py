from django.db import models
from django.contrib.auth.models import AbstractUser
from transliterate import slugify


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='images', blank=True, default='images/default.png')
    nickname = models.CharField(max_length=64, default="")

    def save(self, *args, **kwargs):
        if self.nickname == "":
            self.nickname = self.username

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nickname


class PrivetChat(models.Model):
    chat_path = models.URLField(max_length=200)
    user1 = models.ForeignKey(User, related_name="first", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="second", on_delete=models.CASCADE)


class PrivetMessage(models.Model):
    chat = models.ForeignKey(PrivetChat, on_delete=models.CASCADE)
    message = models.TextField(default="")
    time_in = models.DateTimeField(auto_now_add=True)


class PublicChat(models.Model):
    chat_name = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(unique=True, default='')
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    description = models.CharField(max_length=256, default='Public room')
    host_name = models.CharField(max_length=256, default='')

    def save(self, *args, **kwargs):
        unspace = str(self.chat_name).replace(' ', '-')
        self.slug = unspace if slugify(str(self.chat_name)) is None else slugify(str(self.chat_name))
        self.host_name = self.owner.nickname
        super().save(*args, **kwargs)


class PublicMessage(models.Model):
    chat = models.ForeignKey(PublicChat, on_delete=models.CASCADE)
    message = models.TextField(default="")
    time_in = models.DateTimeField(auto_now_add=True)
