from rest_framework import generics, status, permissions
from .models import BookName, Paragraph, ParagraphStory
from . import serializer


class BookNameListView(generics.ListAPIView):
    queryset = BookName.objects.all()
    serializer_class = serializer.BookNameSerializer


class ParagraphView(generics.ListAPIView):
    serializer_class = serializer.ParagraphSerializer

    def get_queryset(self):
        q = Paragraph.objects.filter(book=self.kwargs.get('id')).all()
        return q


class ParagraphStoryView(generics.RetrieveAPIView):
    serializer_class = serializer.ParagraphStorySerializer
    lookup_field = 'paragraph_id'

    def get_queryset(self):
        q = ParagraphStory.objects.filter(paragraph_id=self.kwargs.get('paragraph_id')).all()
        return q
