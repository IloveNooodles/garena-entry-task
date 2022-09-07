from django.db import models
import logging

log = logging.getLogger()


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
        user = self.objects.filter(referal_code=ref_code)
        if not user.exists():
            return None

        return user.first()

    def find_user_by_username(self, username):
        user = self.objects.filter(username=username)
        if not user.exists():
            return None

        return user

    def filter_user(self, filtered_username):
        list_user = self.objects.filter(username__icontains=filtered_username)
        return list_user
