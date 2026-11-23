from datetime import datetime, timezone

from django.test import TestCase
from django.urls import reverse

from .models import Article, Feedback


class BlogTests(TestCase):
    def setUp(self):
        self.article = Article.objects.create(title='Первая статья', text='Текст статьи')

    def test_all_pages_use_base_template(self):
        for url in (
            reverse('article_list'),
            reverse('article_detail', args=[self.article.pk]),
            reverse('article_new'),
            reverse('article_edit', args=[self.article.pk]),
            reverse('feedback'),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertContains(response, 'Article magazine')
                self.assertContains(response, '<footer')

    def test_date_and_preview(self):
        Article.objects.filter(pk=self.article.pk).update(
            created_at=datetime(2024, 1, 2, tzinfo=timezone.utc)
        )
        long_text = ' '.join(f'слово{i}' for i in range(25))
        Article.objects.filter(pk=self.article.pk).update(text=long_text)

        response = self.client.get(reverse('article_list'))
        self.assertContains(response, '02.01.2024')
        self.assertContains(response, 'слово19')
        self.assertNotContains(response, 'слово20')

    def test_create_article(self):
        response = self.client.post(reverse('article_new'), {
            'title': 'Новая статья',
            'text': 'Содержимое',
            'category': '',
        })
        created = Article.objects.get(title='Новая статья')
        self.assertRedirects(response, reverse('article_detail', args=[created.pk]))

    def test_edit_article(self):
        response = self.client.post(reverse('article_edit', args=[self.article.pk]), {
            'title': 'Изменённая статья',
            'text': 'Новый текст',
            'category': '',
        })
        self.assertRedirects(response, reverse('article_detail', args=[self.article.pk]))
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, 'Изменённая статья')
        self.assertEqual(Article.objects.count(), 1)

    def test_short_title_error_is_shown(self):
        response = self.client.post(reverse('article_new'), {
            'title': 'Тест',
            'text': 'Текст',
            'category': '',
        })
        self.assertContains(response, 'Заголовок должен быть не короче 5 символов.')
        self.assertEqual(Article.objects.count(), 1)

    def test_feedback_saves_and_shows_success_message(self):
        response = self.client.post(reverse('feedback'), {
            'name': 'Иван',
            'email': 'ivan@example.com',
            'message': 'Здравствуйте!',
        }, follow=True)
        self.assertEqual(Feedback.objects.count(), 1)
        feedback = Feedback.objects.get()
        self.assertEqual(feedback.name, 'Иван')
        self.assertEqual(feedback.email, 'ivan@example.com')
        self.assertContains(response, 'Спасибо! Ваше сообщение сохранено.')

    def test_feedback_invalid_email(self):
        response = self.client.post(reverse('feedback'), {
            'name': 'Иван',
            'email': 'не-email',
            'message': 'Здравствуйте!',
        })
        self.assertContains(response, 'invalid-feedback')
        self.assertEqual(Feedback.objects.count(), 0)
