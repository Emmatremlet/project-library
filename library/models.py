
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Media(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    summary = models.TextField()

    class Meta:
        abstract = True


class Book(Media):
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)


class DVD(Media):
    director = models.CharField(max_length=100)
    duration = models.DurationField()


class CD(Media):
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)


class BoardGame(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField()
    summary = models.TextField()
    min_players = models.IntegerField()
    max_players = models.IntegerField()


class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Borrow(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    media = GenericForeignKey('content_type', 'object_id')
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField()

    def __str__(self):
        return f"{self.member} borrowed {self.media}"
