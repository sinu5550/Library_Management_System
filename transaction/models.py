from django.db import models
from account.models import UserProfile
from book.models import Book
# Create your models here.

class Transaction(models.Model):
    account = models.ForeignKey(UserProfile, related_name = 'transaction', on_delete = models.CASCADE) 
    # book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits = 12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)
    
    
    
    class Meta:
        ordering = ['borrowing_date'] 
