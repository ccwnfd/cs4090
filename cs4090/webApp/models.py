from django.db import models
from django.views.generic import TemplateView
from django.utils import timezone
from django.conf import settings

# Create your models here.
class index1(TemplateView):
    template_name = "calendar.html"