from django.db import models


class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    pasword = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    referal_code = models.CharField(max_length=255)
    referred_by = models.BigIntegerField(null=True)
    created_at = models.TimeField(auto_created=True, editable=False)
    updated_at = models.TimeField(auto_created=True, auto_now=True, editable=True)
