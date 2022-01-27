from django.db import models

# Create your models here.
class Content(models.Model):
    
    title = models.CharField(max_length = 80, unique=True, primary_key=True, blank=False)
    story = models.TextField()
    date_published = models.DateField()
    user_id = models.IntegerField()


    def __str__(self):
        return '{} : {} : {} : {}'.format(self.title, self.story, self.date_published, self.user_id)