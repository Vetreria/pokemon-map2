from django.db import models  # noqa F401



class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        if self.title:
            return self.title
        return self.title

# your models here
