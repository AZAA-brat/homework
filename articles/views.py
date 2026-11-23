from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm, FeedbackForm
from .models import Article, Category, Feedback


def article_list(request):
    articles = Article.objects.all()
    q = request.GET.get('q', '')
    if q:
        articles = articles.filter(title__icontains=q)
    return render(request, 'articles/article_list.html', {'articles': articles, 'q': q})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/article_detail.html', {'article': article})


def article_new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, 'Статья создана.')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})


def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, 'Статья обновлена.')
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'articles/article_form.html', {'form': form})


def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'category': category,
    })


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(**form.cleaned_data)
            messages.success(request, 'Спасибо! Ваше сообщение сохранено.')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'articles/feedback.html', {'form': form})
