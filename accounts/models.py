from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('O nome de usuário deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    PUBLISHER = 'publisher'
    READER = 'reader'

    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (PUBLISHER, 'Editor'),
        (READER, 'Leitor'),
    ]

    email = models.EmailField(_('email address'), unique=True)

    role = models.CharField(verbose_name="Papel", max_length=10, choices=ROLE_CHOICES, default=READER)

    plan = models.ForeignKey('core.Plan', verbose_name="Plano", on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Usuário')
        verbose_name_plural = _('Usuários')

    def __str__(self):
        return self.username
