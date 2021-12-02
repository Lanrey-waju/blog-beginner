from django.http import response
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post

# Create your tests here.
class BlogTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@mail.com',
            password='secret'
        )

        self.post=Post.objects.create(
            title='A test title content',
            body='Lorem ipsum dolor sit amet consectetur adipisicing elit. Illum quam voluptatum fugiat dicta debitis. Quod corrupti saepe quas sint debitis!',
            author=self.user
        )

    def test_tring_representation(self):
        post = Post(title='A test title content')
        self.assertEqual(str(post), 'A test title content')

    def test_post_content(self):
        self.assertEqual(self.post.title, 'A test title content')
        self.assertEqual(self.user, 'testuser')
        self.assertEqual(self.post.body, 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Illum quam voluptatum fugiat dicta debitis. Quod corrupti saepe quas sint debitis!')

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Illum quam voluptatum fugiat dicta debitis. Quod corrupti saepe quas sint debitis!')
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response =self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'A test title content')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/post/1/')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'), data={
            'title': 'New title',
            'body': 'New body',
            'author': self.user
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New title')
        self.assertContains(response, 'New body')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_edit', args='1'), data={
            'title': 'Updated title',
            'body': 'Updated body',
        })
        self.assertEqual(response.status_code, 302)

    def test_post_delete_view(self):
        response = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)

    



