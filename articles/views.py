from django.shortcuts import get_object_or_404, render

from .models import Article, Category


def article_list(request):
    articles = Article.objects.all()
    q = request.GET.get('q', '')
    if q:
        articles = articles.filter(title__icontains=q)
    return render(request, 'articles/article_list.html', {'articles': articles, 'q': q})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'category': category,
    })
