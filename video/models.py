from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

User = get_user_model()

class Video(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    video_link = models.URLField(max_length=200)
    short_link = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.CharField(max_length=200)
    likes = models.ManyToManyField(User, related_name="likes")
    dislikes = models.ManyToManyField(User, related_name="dislikes")
    views = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.video_link

    def get_absolute_url(self):
        return reverse("video_details", kwargs={"id": self.pk})
    