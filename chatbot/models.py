from django.db import models

# Create your models here.

class Question(models.Model):
    input_question = models.CharField(max_length=300)
