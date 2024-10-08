from django.db import models

# Create your models here.
class Category(models.Model):
    """
    Model for the categories.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'



