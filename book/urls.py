from django.urls import path
from . import views

urlpatterns = [
    path('details/<int:id>/', views.BookDetailView.as_view(), name='book_details'),
    path('borrow/<int:id>/', views.borrow_now, name='borrow_now'),
]