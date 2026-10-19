from django.test import TestCase
from django.urls import reverse

from .models import Blog


class BlogListDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog = Blog.objects.create(title='Первый блог', content='Текст первого блога')
        cls.blog2 = Blog.objects.create(title='Второй блог', content='Текст второго блога')

    # ---------- ListView ----------
    def test_list_status_code(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_contains_titles(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, 'Первый блог')
        self.assertContains(response, 'Второй блог')

    def test_list_context_has_all_blogs(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(len(response.context['object_list']), 2)

    def test_list_has_links_to_detail(self):
        response = self.client.get(reverse('blog_list'))
        self.assertContains(response, reverse('blog_detail', args=[self.blog.pk]))

    def test_list_link_follows_to_detail(self):
        response = self.client.get(reverse('blog_list'))
        link = reverse('blog_detail', args=[self.blog.pk])
        self.assertContains(response, link)
        detail = self.client.get(link)
        self.assertEqual(detail.status_code, 200)

    # ---------- DetailView ----------
    def test_detail_status_code(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertEqual(response.status_code, 200)

    def test_detail_returns_content(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertContains(response, 'Текст первого блога')

    def test_detail_context_has_correct_id(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertEqual(response.context['object'].id, self.blog.id)

    def test_detail_nonexistent_returns_404(self):
        response = self.client.get(reverse('blog_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_detail_does_not_show_other_blog(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertNotContains(response, 'Текст второго блога')

    def test_detail_uses_correct_template(self):
        response = self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.assertTemplateUsed(response, 'blog/blog_detail.html')


class BlogLikesTests(TestCase):
    def setUp(self):
        self.blog = Blog.objects.create(title='Тест', content='Контент')

    def test_new_blog_has_zero_likes(self):
        self.assertEqual(self.blog.likes, 0)

    def test_detail_view_increments_likes(self):
        self.client.get(reverse('blog_detail', args=[self.blog.pk]))
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.likes, 1)