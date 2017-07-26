from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from ..user_app.models import User
from .models import Book, Author, Review

# Create your views here.
def average_rating():
    for book in Book.objects.all():
        Book.objects.filter(id=book.id).update(average_rating=Review.objects.get_average(book))

def home(request):
    average_rating()
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        context = {'user': user, 'books': Book.objects.all()}
        return render(request, 'book_app/home.html', context)
    else:
        return redirect('user:index')

def log_out(request):
    request.session.flush()
    return redirect('user:index')

def add_book_page(request):
    if 'user_id' in request.session:
        context = {'authors': Author.objects.all()}
        return render(request, 'book_app/add.html', context)
    else:
        return redirect('user:index')

def show_book(request, book_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
        book = Book.objects.get(id=book_id)
        context = {'book': book, 'user': user}
        return render(request, 'book_app/show_book.html', context)
    else:
        return redirect('user:index')

def add_book(request):
    user = User.objects.get(id=request.session['user_id'])
    entry = Book.objects.create_all(request.POST, user)
    if not type(entry) is dict:
        return redirect(reverse('book:show_book', kwargs={'book_id': entry[0].id}))
    else:
        if 'title' in entry:
            messages.add_message(request, messages.INFO, entry['title'], extra_tags='title')
        if 'author' in entry:
            messages.add_message(request, messages.INFO, entry['author'], extra_tags='author')
        if 'review' in entry:
            messages.add_message(request, messages.INFO, entry['review'], extra_tags='review')
        if 'rating' in entry:
            messages.add_message(request, messages.INFO, entry['rating'], extra_tags='rating')
        return redirect(reverse('book:add_book_page'))

def add_review(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    Review.objects.create(review=request.POST['review'], rating=request.POST['rating'],
                            rating_int=int(request.POST['rating']) * '* ', book=book, user=user)
    return redirect(reverse('book:show_book', kwargs={'book_id': book_id}))

def delete_review(request, review_id, book_id):
    Review.objects.get(id=review_id).delete()
    return redirect(reverse('book:show_book', kwargs={'book_id': book_id}))

def view_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {'user': user}
    return render(request, 'book_app/user.html', context)    
