from django.db import models
from django.core.cache import cache
from django.conf import settings
import logging

log = logging.getLogger()
TIMEOUT = 86400  # in second
CACHE_TTL = getattr(settings, "CACHE_TTL", TIMEOUT)


class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    referal_code = models.CharField(max_length=255)
    referred_by = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def find_user_by_ref(self, ref_code):

        if ref_code in cache:
            user = cahce.get(ref_code)
            return user

        user = self.objects.filter(referal_code=ref_code)

        if not user.exists():
            cahce.set(ref_code, None, CACHE_TTL)
            return None

        cache.set(ref_code, user.first(), CACHE_TTL)
        return user.first()

    def find_user_by_username(self, username):
        if username in cache:
            user = cache.get(username)
            return user

        user = self.objects.filter(username=username)
        if not user.exists():
            cache.set(username, None, CACHE_TTL)
            return None

        cache.set(username, user.first(), CACHE_TTL)
        return user.first()

    def filter_user(self, filtered_username):
        list_user = self.objects.filter(username__icontains=filtered_username)
        return list_user
