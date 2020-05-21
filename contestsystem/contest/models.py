from django.db import models
from .validators import validate_statement_extension

# Create your models here.

class Problems(models.Model):
    title = models.CharField(max_length = 20, unique = True)
    time_limit = models.IntegerField(default = 250)
    memory_limit = models.IntegerField(default = 256)
    max_score = models.FloatField(default = 100)
    statements = models.FileField(upload_to = 'statements', validators = [validate_statement_extension])