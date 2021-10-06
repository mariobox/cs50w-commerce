from django import forms
from auctions.models import Listing


# Create the form class.
class CommentForm(forms.Form):
    comment = forms.CharField(required=False, max_length=500, min_length=3, strip=True)

class BidForm(forms.Form):
    bid = forms.DecimalField(required=False, max_digits=7, decimal_places=2)

class CreateListingForm(forms.ModelForm):    
    class Meta:
        model = Listing
        fields = ['title', 'text', 'price', 'image', 'initial_bid', 'category']