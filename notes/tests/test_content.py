from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(title='Заголовок', text='Текст',
                                       slug='note-slug', author=cls.author)

    def test_pages_contains_form(self):
        """На страницы создания и редактирования заметки передаются формы."""
        self.client.force_login(self.author)
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_in_list_for_author(self):
        """Заметка передается в список заметок в словаре context для автора."""
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.object_list = response.context['object_list']
        self.assertIn(self.note, self.object_list)

    def test_note_not_in_list_for_another_user(self):
        """
        Заметка не передается в список заметок в словаре context
        для не автора.
        """
        self.client.force_login(self.not_author)
        url = reverse('notes:list')
        response = self.client.get(url)
        self.object_list = response.context['object_list']
        self.assertNotIn(self.note, self.object_list)
