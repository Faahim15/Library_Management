from django import forms 
from . models import AccountModel


from django import forms

class ReviewForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 12, 'class': 'bg-blue-100 text-red-500 border rounded-md p-2 focus:outline-none focus:border-blue-500 italic'}))
    RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)



class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)





