from django.db import models
import uuid
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,email,username,password=None,password1=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.is_normalusers=True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):

    class Meta:
        db_table = 'Users'

    email = models.EmailField(max_length=200, unique=True, editable=True)
    username = models.CharField(max_length=100, unique=True)
    LastLogin = models.DateTimeField(auto_now=True)

    is_active= models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    is_normalusers=models.BooleanField(default=False)
    is_staffusers=models.BooleanField(default=False)
    otp=models.IntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        if self.is_admin or self.is_staffusers:
           return True
        else:
            return False
    
    