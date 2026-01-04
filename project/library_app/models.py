from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"
    
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

class Genre(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    summary = models.TextField()
    isbn = models.CharField('ISBN', max_length=13, unique=True)
    publication_year = models.IntegerField()
    publisher = models.CharField(max_length=200, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    membership_date = models.DateField(auto_now_add=True)
    card_number = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.card_number})"

class BookInstance(models.Model):
    STATUS_CHOICES = [
        ('a', 'Available'),
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('r', 'Reserved'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    inventory_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a')
    due_back = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['due_back']
    
    def __str__(self):
        return f"{self.inventory_number} ({self.book.title})"