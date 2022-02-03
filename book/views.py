from rest_framework import generics, status, permissions, pagination
from .models import BookName, Paragraph, ParagraphStory, Author, Dictionary
from . import serializer
from rest_framework.viewsets import  ModelViewSet


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


class DictionaryView(ModelViewSet):
    serializer_class = serializer.DictionarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        q = Dictionary.objects.filter(user_id=self.request.user.pk)
        return q


class FilterByParagraph(generics.ListAPIView):
    serializer_class = serializer.DictionarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        q = Dictionary.objects.filter(paragraph_id=self.kwargs.get('paragraph_id')).all()
        return q
