# Generated by Django 4.0.1 on 2022-02-08 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0002_dictionary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_right_answer', models.BooleanField(verbose_name='სწორი პასუხია?')),
            ],
            options={
                'verbose_name': 'ქვიზი',
            },
        ),
        migrations.AlterField(
            model_name='dictionary',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='დამატების თარიღი'),
        ),
        migrations.AddIndex(
            model_name='dictionary',
            index=models.Index(fields=['in_english', 'in_english'], name='book_dictio_in_engl_fee940_idx'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='paragraph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='book.paragraph', verbose_name='პარაგრაფი'),
        ),
        migrations.AddField(
            model_name='quiz',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='მომხმარებელი'),
        ),
    ]
