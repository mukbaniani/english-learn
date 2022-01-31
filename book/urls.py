from django.urls import path
from . import views

urlpatterns = [
    path('list-book/', views.BookNameListView().as_view(), name='book-list'),
    path('paragraph-list/<int:id>/', views.ParagraphView().as_view(), name='paragraph-list'),
    path('story/<int:paragraph_id>/', views.ParagraphStoryView().as_view(), name='paragraph-story')
]