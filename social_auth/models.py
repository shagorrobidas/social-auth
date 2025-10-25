from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    current_refresh_token = models.TextField(blank=True, null=True)
    force_logout_required = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class SocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=255)
    extra_data = models.JSONField(default=dict)

    class Meta:
        unique_together = ('provider', 'uid')
        verbose_name = _('Social Account')
        verbose_name_plural = _('Social Accounts')

    def __str__(self):
        return f'{self.user.email} - {self.provider.capitalize()}'
