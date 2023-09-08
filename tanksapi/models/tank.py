from django.db import models


class Tank(models.Model):
    profile = models.ForeignKey(
        "Profile", on_delete=models.CASCADE, related_name='owned_tanks')
    name = models.CharField(max_length=75)
    gallons = models.IntegerField(4)
    flora = models.TextField()
    fauna = models.TextField()
    started_date = models.CharField(max_length=10)
    noteworthy_comments = models.TextField()
    photo_url = models.URLField(max_length=200)
    tags = models.ManyToManyField("Tag", related_name="tanks_with_tag")
