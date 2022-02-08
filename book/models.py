from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('სახელი'))
    last_name = models.CharField(max_length=50, verbose_name=_('გვარი'))
    date_of_birth = models.DateField(verbose_name=_('დაბადების თარიღი'))

    class Meta:
        verbose_name = _('ავტორები')

    def __str__(self):
        return f"{self.__class__.__name__}('{self.name}', '{self.last_name}')"


class BookName(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('სახელი'))
    image = models.ImageField(verbose_name=_('სურათი'), upload_to='images')
    description = models.TextField(verbose_name=_('აღწერა'))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=_('ავტორი'))

    class Meta:
        verbose_name = _('წიგნი')

    def __str__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Paragraph(models.Model):
    title = models.CharField(max_length=60, verbose_name=_('პარაგრაფის სათაური'))
    book = models.ForeignKey(BookName, on_delete=models.CASCADE, verbose_name=_('წიგნი'))

    class Meta:
        verbose_name = _('პარაგრაფები')

    def __str__(self):
        return f"{self.__class__.__name__}('{self.title}')"


class ParagraphStory(models.Model):
    story = models.TextField(verbose_name=_('ამბავი'))
    paragraph_id = models.OneToOneField(Paragraph, on_delete=models.CASCADE, verbose_name=_('პარაგრაფი'))

    class Meta:
        verbose_name = _('ამბები')

    def __str__(self):
        return f"{self.__class__.__name__}('{self.story}')"


class Dictionary(models.Model):
    in_english = models.CharField(max_length=255, verbose_name=_('ინგლისური'))
    in_georgian = models.CharField(max_length=255, verbose_name=_('ქართულად'))
    datetime = models.DateTimeField(default=timezone.now, verbose_name=_('დამატების თარიღი'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('მფლობელი'))
    paragraph = models.ForeignKey(Paragraph, on_delete=models.DO_NOTHING, blank=True,  null=True, verbose_name=_('პარაგრაფი'))

    class Meta:
        verbose_name = _('ლექსიკონი')
        indexes = [
            models.Index(fields=['in_english', 'in_english'])
        ]

    def __str__(self):
        return f"{self.__class__.__name__}('{self.in_english}' -> '{self.in_georgian}')"


class Quiz(models.Model):
    is_right_answer = models.BooleanField(verbose_name=_('სწორი პასუხია?'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('მომხმარებელი'))
    paragraph = models.ForeignKey(Paragraph, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name=_('პარაგრაფი'))

    def __str__(self):
        return f"{self.__class__.__name__}('{self.user.name}' -> {self.is_right_answer})"

    class Meta:
        verbose_name = _('ქვიზი')
