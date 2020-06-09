import os
import uuid

from django.db import models
from .validators import validate_statement_extension
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Problems(models.Model):
    title = models.CharField(max_length = 20, unique = True)
    time_limit = models.IntegerField(default = 250)
    memory_limit = models.IntegerField(default = 256)
    max_score = models.FloatField(default = 100)
    statements = models.FileField(upload_to = 'statements', validators = [validate_statement_extension])

    def __str__(self):
        return self.title
    

@receiver(models.signals.post_delete, sender = Problems)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.statements:
        if os.path.isfile(instance.statements.path):
            os.remove(instance.statements.path)

@receiver(models.signals.pre_save, sender = Problems)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Problems.objects.get(pk=instance.pk).statements
    except Problems.DoesNotExist:
        return False

    new_file = instance.statements
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Submission(models.Model):
    date = models.DateTimeField(auto_now_add = True)
    user = models.CharField(max_length = 150)
    problem = models.CharField(max_length = 20)
    language = models.CharField(max_length = 20)
    verdict = models.IntegerField(default = 0)
    runTime = models.IntegerField(default = 0)
    memory = models.IntegerField(default = 0)
    source_code = models.TextField(null = True)
    log = models.TextField(null = True)