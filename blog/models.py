# blog/models.py

from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
            "auth.User",
            on_delete = models.CASCADE,
        )
    body = models.TextField()

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return reverse("post_detail", kwargs = {"pk" : self.pk} )
