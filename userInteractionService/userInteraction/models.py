from django.db import models

class LikeEvent(models.Model):
    user_id = models.IntegerField(blank=False)
    title = models.CharField(max_length=80)

#Operating under the assumption that user can read book more than once
class ReadEvent(models.Model):
    user_id = models.IntegerField(blank = False)
    title = models.CharField(max_length=80)
    countReads = models.IntegerField(blank=True)

class User(models.Model):
    id = models.IntegerField(primary_key=True)
