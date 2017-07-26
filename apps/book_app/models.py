from __future__ import unicode_literals
from django.db import models
from ..user_app.models import User

# Create your models here.
class ReviewManager(models.Manager):
    def get_average(self, book):
        total_reviews = self.filter(book=book)
        total = 0
        for review in total_reviews:
            total += int(review.rating)
        avg = total / total_reviews.count()
        return avg * '* '

class BookManager(models.Manager):
    def create_all(self, data, user):
        errors = {}
        if not data['title']:
            errors['title'] = 'Enter Book Title'
        if not data['existing_author'] and not data['new_author']:
            errors['author'] = 'Enter or Select Author name'
        if not data['review']:
            errors['review'] = 'Enter a review'
        if not data['rating'] or not len(data['rating']):
            errors['rating'] = 'Select a rating'
        if len(errors):
            return errors
        else:
            current_author = data['existing_author']
            if data['new_author']:
                current_author = data['new_author']
            if Author.objects.filter(name=current_author):
                author = Author.objects.get(name=current_author)
                if self.filter(title=data['title'], author=author):
                    book = self.get(title=data['title'], author=author)
                    review = Review.objects.create(review=data['review'], rating=data['rating'],
                                                    rating_int=int(data['rating']), book=book, user=user)
                    return [book, review]
                else:
                    book = self.create(title=data['title'], author=author)
                    review = Review.objects.create(review=data['review'], rating=data['rating'],
                                                    rating_int=int(data['rating']), book=book, user=user)
                    return [book, review]
            else:
                author = Author.objects.create(name=current_author)
                book = self.create(title=data['title'], author=author)
                review = Review.objects.create(review=data['review'], rating=data['rating'],
                                                rating_int=int(data['rating']) * '* ', book=book, user=user)
                return [book, review]


class Author(models.Model):
    name = models.CharField(max_length=30)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='books')
    average_rating = models.CharField(max_length=100, default='')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    review = models.TextField(max_length=1000)
    rating = models.CharField(max_length=20)
    rating_int = models.CharField(max_length=20)
    book = models.ForeignKey(Book, related_name='book_reviews')
    user = models.ForeignKey(User, related_name='user_reviews')
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ReviewManager()
