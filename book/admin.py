from django.contrib import admin
from .models import Paragraph, ParagraphStory, BookName, Author, Dictionary

admin.site.register([Paragraph, ParagraphStory, BookName, Author, Dictionary])
