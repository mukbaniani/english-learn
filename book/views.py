from rest_framework import generics, status, permissions
from .models import BookName, Paragraph, ParagraphStory, Author
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


class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = serializer.AuthorSerializer


class RetrieveAuthor(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = serializer.AuthorSerializer
    lookup_field = 'id'


class GetBookByCategory(generics.ListAPIView):
    serializer_class = serializer.BookNameSerializer

    def get_queryset(self):
        q = BookName.objects.filter(author_id=self.kwargs.get('author_id')).all()
        return q
