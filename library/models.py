
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Media(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        abstract = True


class Book(Media):
    author = models.CharField(max_length=100)
    borrow_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)


class DVD(Media):
    director = models.CharField(max_length=100)
    borrow_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)


class CD(Media):
    artist = models.CharField(max_length=100)
    borrow_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)


class BoardGame(Media):
    creator = models.CharField(max_length=100)


class MemberManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class Member(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)


    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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



