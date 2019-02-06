from django.urls import path

from authors.apps.articles import views
from .models import Article, Reaction

app_name = "articles"

urlpatterns = [
    path('articles/', views.ListCreateArticle.as_view(), name='articles'),
    path('articles/<slug>/', views.RetrieveUpdateDeleteArticle.as_view(),
         name='article-details'),
    path('articles/<slug>/like/', views.ReactionView.as_view(
        model=Article, reaction_type=Reaction.LIKE),
        name='like-article'),
    path('articles/<slug>/dislike/', views.ReactionView.as_view(
        model=Article, reaction_type=Reaction.DISLIKE),
        name='dislike-article'),
    path('article/search/', views.ArticleList.as_view(), name='article-search')
]
