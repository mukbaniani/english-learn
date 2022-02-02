from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('dict-list', views.DictionaryView, basename='dict-list')

urlpatterns = [
    path('list-book/', views.BookNameListView().as_view(), name='book-list'),
    path('paragraph-list/<int:id>/', views.ParagraphView().as_view(), name='paragraph-list'),
    path('story/<int:paragraph_id>/', views.ParagraphStoryView().as_view(), name='paragraph-story'),
    path('author-list/', views.AuthorList().as_view(), name='author-list'),
    path('author-retrieve/<int:id>/', views.RetrieveAuthor().as_view(), name='author-retrieve'),
    path('get-book-by-author/<int:author_id>/', views.GetBookByCategory().as_view(), name='get-book-by-author')
] + router.urls