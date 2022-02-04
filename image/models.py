from django.db import models

# Create your models here.

TEMP = 'TEMPORARY'
PERM = 'PERMANENT'


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Image-{self.id}'
