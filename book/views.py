from django.shortcuts import render,redirect
from . import models
from . import forms
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from transaction.views import send_transaction_email
# Create your views here.

class BookDetailView(DetailView):
    model = models.Book
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
        return redirect('book_details', id=book.id)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object 
        comments = book.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


@login_required
def borrow_now(request, id):
    book = models.Book.objects.get(pk=id)
    
    if request.user.account.balance < book.borrowing_price:
        messages.error(request, 'Insufficient balance to borrow the book.')
        return redirect('book_details', id=id)
    
    request.user.account.balance -= book.borrowing_price
    request.user.account.save()

    borrowed_book=models.userBorrowed.objects.create(
        author=request.user,
        book=book,
        price=book.borrowing_price
    )
    book.save()
    send_transaction_email(request.user, borrowed_book.price, "Borrowing Message", "borrow_email.html")
    messages.success(request, 'Book Borrowing Succeded!')
       
    return redirect('book_details', id=id)