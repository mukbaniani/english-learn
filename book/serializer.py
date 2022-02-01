from rest_framework import serializers
from .models import BookName, Paragraph, ParagraphStory, Author


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
