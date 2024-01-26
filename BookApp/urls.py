from django.urls import path 
from . views import DetailsBookView,Borrow_Books,Deposit_money,Order_history,ReturnBook,leave_review
urlpatterns = [
    path('details/<int:id>/',DetailsBookView.as_view(), name='book_details'), 
    path('borrowed_book/<int:id>/',Borrow_Books, name='borrowed_book'),
    path('deposit_money/',Deposit_money, name='Deposit_money'), 
    path('profile/',Order_history,name='profile'),
    path('profile/review/<int:order_id>/',leave_review,name='review'),
    path("return_loans/<int:loan_id>/", ReturnBook.as_view(), name="pay_loan"),
    
] 