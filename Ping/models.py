from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name = "followed_by",
        symmetrical= False,
        blank = True
    )
    def __str__(self):
        return self.user.username

@receiver(post_save, sender = User)   
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()


class Pings(models.Model):
    user = models.ForeignKey(
        User, related_name = "pinged" , on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add= True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank= True, null=True, related_name= 'children')
    likes = models.ManyToManyField(User, blank=True, null=True, related_name='liked')

    def total_likes(self):
        return self.likes.count()

    def __str__(self) -> str:
        return (
            f"{self.user}"
            f"{self.created_on:%Y-%m-%d %H:%M}"
            f"{self.body[:15]}"
            )

#post_save.connect(create_profile, sender = User)