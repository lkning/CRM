from django.db import models

# Create your models here.

class Role(models.Model):
    caption = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "角色表"

    def __str__(self):
        return self.caption
class UserType(models.Model):
    title = models.CharField(max_length=32)
    roles = models.ManyToManyField(to=Role)

    def __str__(self):
        return self.title
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32)
    ut = models.ForeignKey(to=UserType,null=True,blank=True)
