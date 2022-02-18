from django.db import models


class Commit(models.Model):
    author = models.CharField(max_length=200, blank=False, null=False)
    date = models.DateTimeField()
    message = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.message


class Project(models.Model):
    url = models.URLField(max_length=400)
    name = models.CharField(max_length=200, blank=False, null=False)
    org = models.CharField(max_length=200)
    commit = models.ForeignKey(Commit, on_delete=models.CASCADE, related_name="commits")
    language = models.CharField(max_length=200)
    stars = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now_add=True)
    download_link = models.URLField()

    def __str__(self):
        return self.name
