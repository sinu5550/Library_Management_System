from django.db import models
from category.models import Category
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ManyToManyField(Category) 
    borrowing_price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='book/media/uploads/', blank = True, null = True)
    def __str__(self):
        return self.title

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.title}"
    

class userBorrowed(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    borrowing_date = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return f"{self.author.username} borrowed Book: {self.book.title}"