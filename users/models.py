from tabnanny import verbose
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
#local imports
from base_model.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an username address')

        user = self.model(
            username=username.strip(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given username, date of
        birth and password.
        """
        user = self.create_user(
            username,
            password=password
        )
        user.is_superuser= True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):  #
       
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    #permissions
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        else:
            return self.username
    # @property
    # def docs(self):
    #     return self.document.first()
    @property
    def full_name(self):
        try:
            return f"{self.last_name} {self.first_name} {self.father_name}"
        except:
            return self.username


class UserDocs(BaseModel):
    GENRE = (
        ('e', 'Мужской'),
        ('a', 'Женский')
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    genre = models.CharField(max_length=2,null=True, blank=True, choices=GENRE, verbose_name="Пол")
    nationality = models.CharField(max_length=200, verbose_name="Национальность", null=True, blank=True)
    citizen = models.CharField(max_length=120, verbose_name="Гражданство", null=True, blank=True)
    state = models.CharField(max_length=200, verbose_name="Область рождения", null=True, blank=True)
    region = models.CharField(max_length=100, verbose_name="Район рождения", null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="document")
    doc_type = models.CharField(max_length=220, verbose_name="Тип документа", null=True, blank=True)
    pinfl = models.CharField(max_length=70, verbose_name="ПИНФЛ", null=True, blank=True)
    serial = models.CharField(max_length=15, verbose_name="Серия", null=True, blank=True)
    doc_number = models.CharField(max_length=30, verbose_name="Номер документа", null=True, blank=True)
    who_gave = models.CharField(max_length=300, verbose_name="Кем выдан", null=True, blank=True)
    school = models.CharField(max_length=300, verbose_name="Организация", null=True, blank=True)
    klass = models.CharField(max_length=20, default=None, null=True, blank=True)
    state_organ = models.CharField(max_length=100, verbose_name="Область организации", null=True, blank=True)
    region_organ = models.CharField(max_length=100, verbose_name="Регион организации", null=True, blank=True)

    class Meta:
        verbose_name = _("Student Info")
        verbose_name_plural = _("Student Infos")

    def __str__(self):
        return self.user.full_name