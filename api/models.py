from django.db import models
import logging

log = logging.getLogger()
class User(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    referal_code = models.CharField(max_length=255)
    referred_by = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)
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
        try:
            user = self.objects.get(ref_code=ref_code)
            return user
        except Exception as e:
            log.error(str(e))
            return None

    def find_user_by_username(self, username):
        try:
            user = self.objects.get(username=username)
            return user
        except Exception as e:
            log.error(str(e))
            return None
