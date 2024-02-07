from django.db import models

class Knowledge(models.Model):
    titile = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.titile