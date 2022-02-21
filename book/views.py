from rest_framework import generics, status, permissions
from .models import BookName, Paragraph, ParagraphStory, Author, Dictionary, Quiz, User
from . import serializer
from rest_framework.viewsets import  ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from rest_framework.response import Response


class BookNameListView(generics.ListAPIView):
    queryset = BookName.objects.all()
    serializer_class = serializer.BookNameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class RetrieveAuthor(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = serializer.AuthorSerializer
    lookup_field = 'id'


class GetBookByCategory(generics.ListAPIView):
    serializer_class = serializer.BookNameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def get_queryset(self):
        q = BookName.objects.filter(author_id=self.kwargs.get('author_id')).all()
        return q


class DictionaryView(ModelViewSet):
    serializer_class = serializer.DictionarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['in_english', 'in_georgian']

    def get_queryset(self):
        q = Dictionary.objects.filter(user_id=self.request.user.pk)
        return q


class FilterByParagraph(generics.ListAPIView):
    serializer_class = serializer.DictionarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['in_english', 'in_georgian']

    def get_queryset(self):
        q = Dictionary.objects.filter(paragraph_id=self.kwargs.get('paragraph_id')).all()
        return q


class QuizView(generics.ListCreateAPIView):
    queryset = Dictionary.objects.all()
    serializer_class = serializer.QuizFormSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        paragraph_id = Paragraph.objects.filter(id=self.kwargs.get('paragraph_id')).first()
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        in_english = serializer.validated_data.get("in_english")
        in_georgian = serializer.validated_data.get("in_georgian")
        dict_list = Dictionary.objects.filter(Q(in_english=in_english) & Q(in_georgian=in_georgian)).exists()
        if dict_list:
            Quiz.objects.create(is_right_answer=True, user=user, paragraph=paragraph_id)
            return Response({"result": "პასუხი სწორია"}, status=status.HTTP_200_OK)
        else:
            Quiz.objects.create(is_right_answer=False, user=user, paragraph=paragraph_id)
            return Response({"result": "პასუხი არასწორია"}, status=status.HTTP_200_OK)


class QuizStat(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializer.StatSerializer

    def get_queryset(self):
        q = User.objects.filter(pk=self.request.user.id).annotate(
            right=Count('quiz', filter=Q(quiz__is_right_answer=True)),
            wrong=Count('quiz', filter=Q(quiz__is_right_answer=False)),
        )
        return q
