from django.test import TestCase

# Create your tests here.
from .models import Image, Mission
from django.conf import settings
import os

root_node = Mission.objects.all()[0]
root_node.image_path = settings.MEDIA_ROOT
