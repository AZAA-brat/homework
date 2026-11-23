from django.urls import path

from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/new/', views.article_new, name='article_new'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('feedback/', views.feedback, name='feedback'),
]
