from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from .models import Borrow, Member, Book
from django.urls import reverse

class BorrowModelTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            is_active=True
        )
        
        self.book = Book.objects.create(
            title='Test Book',
            author='Author Name',
            is_borrowed=False,  
        )
        
        self.borrow = Borrow.objects.create(
            member=self.member,
            content_type=ContentType.objects.get_for_model(self.book),
            object_id=self.book.id,
            borrow_date=timezone.now().date() - timedelta(days=8),  
            return_date=timezone.now().date() - timedelta(days=1)  
        )
        
        self.borrow2 = Borrow.objects.create(
            member=self.member,
            content_type=ContentType.objects.get_for_model(self.book),
            object_id=self.book.id,
            borrow_date=timezone.now().date() - timedelta(days=8),  
            return_date=timezone.now().date() - timedelta(days=3)  
        )
        
    def test_cannot_borrow_with_late_return(self):
        self.client.login(username='johndoe', password='password')
        
        response = self.client.post(reverse('borrow_create'), data={
            'member': self.member.id,
            'media': self.book.id,
            'media_type': 'book',
        }, follow=True)
        
        self.assertEqual(response.status_code, 302) 
        # self.assertContains(response, 'Vous avez au moins un emprunt en retard.', status_code=302)
        self.assertEqual(Borrow.objects.count(), 1)

