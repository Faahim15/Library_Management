from django.shortcuts import get_object_or_404,render,redirect
from django.views.generic import CreateView,DetailView 
from .models import BooksModel, AccountModel,OrderBooks,Review
from . forms import  DepositForm,ReviewForm
from django.contrib import messages 
from decimal import Decimal 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views import View 
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here. 
def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
class DetailsBookView(DetailView):
    model = BooksModel 
    pk_url_kwarg = 'id'
    template_name = 'books_details.html' 
    context_object_name = 'data'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object 
        reviews = Review.objects.filter(book=book)
        context['reviews'] = reviews
        return context
    
        

     
    
     

def Borrow_Books (request, id):
    obj = get_object_or_404(BooksModel, pk=id)
    existing_order = OrderBooks.objects.filter(borrowed_books=obj, customer=request.user).first()
    if existing_order:
        messages.success(request, 'You have already bought this book.')
        return redirect('profile')
    else:

        if request.method == 'POST':
            price = obj.book_price 
            balance = request.user.account.balance 
            
            if price <= balance:
                new_balance = balance - price 
                account, created = AccountModel.objects.get_or_create(user_acc=request.user) 
                account.balance = new_balance
                account.save() 
                OrderBooks.objects.create( borrowed_books =obj, customer = request.user,balance_after_transaction = new_balance )
    
            else: 
                messages.success(request, 'Insufficient balance.') 

        return redirect('profile')  

def Deposit_money(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = DepositForm(request.POST) 
            if form.is_valid(): 
                deposit = form.cleaned_data['amount'] 
                amount = Decimal(deposit) 
                if amount < 100:
                    messages.success(request, 'Transaction Alert: Insufficient funds. Please ensure your deposit exceeds $100 for successful processing.') 
                else:
                    user_model_instance, created = AccountModel.objects.get_or_create(user_acc=request.user) 
                    if user_model_instance.balance is not None:
                        user_model_instance.balance += amount 
                    else: 
                        user_model_instance.balance = amount 
                    user_model_instance.save()
                    messages.success(request, 'Deposit successful!') 
                    send_transaction_email(request.user, amount, "Deposite Message", "deposit_email.html")
                    return redirect('homepage')
    else:
        form = DepositForm() 
    return render(request, 'deposit_money.html',{'form':form})



def Order_history(request):

    orders = OrderBooks.objects.filter(customer = request.user).order_by('order_date') 
    
    return render(request, 'profile.html', {'orders': orders})   

class ReturnBook(LoginRequiredMixin, View):
    def get(self, request, loan_id):
        loan = get_object_or_404(BooksModel, id=loan_id) 
        order_book = get_object_or_404(OrderBooks,customer = request.user,borrowed_books = loan)
        amount = loan.book_price 
        check = request.user.account 
        if amount <= check.balance and order_book.is_paid == False:  
            check.balance += amount 
            order_book.is_paid = True  
            order_book.save()
            check.save() 

            messages.success(request, f'Payment successful ${amount}. You have successfully returned the borrowed books.') 
        else: 
            messages.error(request, 'Insufficient balance or payment already clear.')

        return redirect('profile') 


def leave_review(request, order_id):
    order = get_object_or_404(OrderBooks, id=order_id, customer=request.user)
    existing_review = Review.objects.filter(book_order=order, user=request.user).first() 
    if existing_review:
        
        messages.info(request, 'You have already reviewed this book.')
        return redirect('profile')
    else:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                rating = form.cleaned_data['rating']
                
                Review.objects.create(book_order=order, user=request.user, book=order.borrowed_books, content=content, rating=rating)
                
                messages.success(request, 'Thank you for your review!')
                return redirect('homepage')
        else:
            form = ReviewForm()

        return render(request, 'leave_review.html', {'form': form, 'order': order})