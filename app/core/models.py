from django.db import models
from django.utils import timezone
import string
import random

class UrlManager(models.Manager):
  def create_url(self, original_url):
    shortened_code = self.generate_unique_code()
    if not original_url or original_url == '':
      raise ValueError('a Url must be entered.')
    return self.create(original_url=original_url, shortened_code=shortened_code)

  def generate_unique_code(self, length=6):
    characters = string.ascii_letters + string.digits
    while True:
      code = ''.join(random.choices(characters, k=length))
      if not self.filter(shortened_code=code).exists():
        return code

class Url(models.Model):
    url_id = models.AutoField(primary_key=True)
    original_url = models.URLField(max_length=255, unique=True)
    shortened_code = models.CharField(max_length=20, unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    last_accessed = models.DateTimeField(null=True, blank=True)

    objects = UrlManager()
