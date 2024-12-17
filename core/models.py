from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    ratings_count = models.IntegerField(default=0)
    ratings_sum = models.IntegerField(default=0)

    @property
    def average_rating(self):
        if self.ratings_count == 0:
            return 0
        return self.ratings_sum / self.ratings_count

    def __str__(self):
        return self.title


class Rating(models.Model):
    user = models.ForeignKey("core.User", on_delete=models.CASCADE, related_name="ratings")
    article = models.ForeignKey("core.Article", on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField()

    class Meta:
        unique_together = ("user", "article")

    def __str__(self):
        return f"{self.user.username} rated {self.article.title} - {self.score}"
