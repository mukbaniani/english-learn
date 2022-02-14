from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import BookName, Paragraph, ParagraphStory, Author, Dictionary


class BookNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookName
        fields = '__all__'


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = '__all__'


class ParagraphStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParagraphStory
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['in_english', 'in_georgian', 'user', 'paragraph']


class StatSerializer(serializers.Serializer):
    right = serializers.CharField(label=_('სწორი პასუხები'), read_only=True)
    wrong = serializers.CharField(label=_('არასოწორი პასუხები'), read_only=True)
