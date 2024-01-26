from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.
class CategoryModel(models.Model):
    books_category = models.CharField(max_length =100) 
    slug = models.SlugField(max_length=100,unique=True, null=True, blank=True)  

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.books_category)
        super().save(*args, **kwargs)
    def __str__(self):
        return self.books_category 

class BooksModel(models.Model):
    books = models.ForeignKey(CategoryModel, on_delete = models.CASCADE)
    title = models.CharField(max_length=100) 
    description = models.TextField() 
    book_price = models.PositiveIntegerField() 
    image = models.ImageField(upload_to='Core/media/uploads/', blank = True, null = True) 
    

    def __str__(self):
        return self.title 

class AccountModel (models.Model): 
    user_acc = models.OneToOneField(User,  on_delete=models.CASCADE,related_name='account')
    balance = models.DecimalField(max_digits=12, decimal_places=2,null=True,default = 100) 
    
    

 

class OrderBooks (models.Model):
    borrowed_books = models.ForeignKey(BooksModel, on_delete = models.CASCADE) 
    customer = models.ForeignKey(User, on_delete = models.CASCADE)  
    balance_after_transaction = models.DecimalField(max_digits=10, decimal_places=2,null = True, blank = True) 
    is_paid = models.BooleanField(default=False)
    order_date =models.DateTimeField(default =timezone.now) 
    def __str__(self):
        return f"Books title {self.borrowed_books}"

class Review(models.Model):
    book_order = models.OneToOneField(OrderBooks, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BooksModel, on_delete=models.CASCADE ,null =True, blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5) 
    created_on =models.DateTimeField(default =timezone.now)
    
    def __str__(self):
        return f"Comments by {self.user.username}"


