from django.db import models

from mptt.models import MPTTModel
from django.conf import settings
# Create your models here.


class Mission(MPTTModel):
    name = models.TextField(default="new task")
    info = models.TextField(default=0)
    user = models.TextField(default="root")
    date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=True)

    parent_mission_id = models.IntegerField(default=0)
    image_path = models.TextField(default=settings.MEDIA_ROOT)

    image_num = models.IntegerField(default=0)
    # image_list = models.FilePathField(path=settings.MEDIA_ROOT, recursive=False)
    detect_path = models.TextField(default=settings.DETECT_ROOT)
    seg_path = models.TextField(default=settings.SEG_ROOT)

    class MPTTMeta:
        parent_attr = 'parent'

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.TextField()
    img = models.ImageField(upload_to="img/")
    image_id = models.IntegerField()
    width = models.IntegerField(default=None)
    height = models.IntegerField(default=None)
    detect_result = models.NullBooleanField(default=None)
    # seg_result = models.ImageField(default=None)

    def __str__(self):
        return self.name
