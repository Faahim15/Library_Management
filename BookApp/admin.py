from django.contrib import admin
from . models import BooksModel,CategoryModel,AccountModel,OrderBooks,Review
# Register your models here. 
admin.site.register(BooksModel)
admin.site.register(CategoryModel)
admin.site.register(AccountModel)
admin.site.register(OrderBooks)
admin.site.register(Review)
