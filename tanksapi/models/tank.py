from django.db import models


class Tank(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name='owned_tanks')
    name = models.CharField(max_length=75)
    gallons = models.IntegerField(4)
    flora = models.CharField(max_length=400)
    fauna = models.CharField(max_length=400)
    started_date = models.CharField(max_length=10)
    noteworthy_comments = models.CharField(max_length=400)
    photo_url = models.URLField(max_length=200)
    tags = models.ManyToManyField("Tag")
