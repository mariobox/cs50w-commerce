from auctions.models import Listing, Comment, Favorite, Bid, Category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import User
from auctions.forms import CommentForm
from auctions.forms import BidForm
from auctions.forms import CreateListingForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError


class ListingListView(ListView):
    model: Listing
    template_name = "auctions/listing_list.html"
    def get(self, request) :
        listing_list = Listing.objects.all().filter(active=True)
        ctx = {'listing_list' : listing_list }
        return render(request, self.template_name, ctx)

class FavoriteListView(ListView):
    template_name = "auctions/favorite_list.html"
    def get(self, request):
        listing_list = Listing.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_listings.values('id')   
            favorites = [ row['id'] for row in rows ] 
            print(favorites)  
            ctx = {
                'listing_list': listing_list,
                'favorites': favorites,
            }
            return render(request, self.template_name, ctx)


class ListingDetailView(DetailView):
    model: Listing
    template_name = "auctions/listing_detail.html"

    def get(self, request, pk) :
        x = Listing.objects.get(id=pk)
        comment_form = CommentForm()
        bid_form = BidForm()
        comments = Comment.objects.filter(listing=x).order_by('-updated_at')
        bids = Bid.objects.filter(listing=x)     
        last_bid = Bid.objects.filter(listing=x).last()        
        high_bid = Bid.objects.filter(listing=x).order_by('-amount').first()         
        if len(bids) == 0:
            current_bid = 0
            message =  "There are no bids for this item."  
            message_type = 'alert alert-warning'       
        else:
            current_bid = high_bid.amount             
            if request.user == high_bid.owner:
                message = "You are currently the highest bidder."
                message_type = 'alert alert-success'
            else:
                message = f"You need to bid more than ${high_bid.amount}." 
                message_type = 'alert alert-danger'         
        
        # Pass favorites
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_listings.values('id')   
            favorites = [ row['id'] for row in rows ]   
            print(f'{x.id} in {favorites}')
            print(f'{x.category}')
            

        context = { 
            'listing': x, 
            'comments': comments, 
            'comment_form': comment_form, 
            'bids': bids, 
            'bid_form' : bid_form, 
            'high_bid': high_bid, 
            'current_bid': current_bid, 
            'message': message,             
            'message_type': message_type,
            'favorites': favorites
            }
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        x = Listing.objects.get(id=pk)
        x.active = False
        x.save()
        return redirect(reverse('auctions:listing_detail', args=[pk]))

class ListingCreateView(LoginRequiredMixin, View): 
    template_name = 'auctions/listing_form.html'
    success_url = reverse_lazy('auctions:index')

    def get(self, request, pk=None):
        listing_form = CreateListingForm()
        ctx = {'listing_form': listing_form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        listing_form = CreateListingForm(request.POST, request.FILES or None)

        if not listing_form.is_valid():
            ctx = {'listing_form': listing_form}
            return render(request, self.template_name, ctx)

        # Adding owner to the model before saving
        inst = listing_form.save(commit=False)
        inst.owner = self.request.user
        inst.save()
        listing_form.save()

        return redirect(self.success_url)


class ListingUpdateView(UpdateView):
    pass

class ListingDeleteView(DeleteView):
    pass

class CommentCreateView(LoginRequiredMixin, View):
    login_url = '/login'
    def post(self, request, pk) :        
        f = get_object_or_404(Listing, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, listing=f)
        comment.save()
        return redirect(reverse('auctions:listing_detail', args=[pk]))

class CommentDeleteView(ListingDeleteView):
    model = Comment
    template_name = "auctions/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        listing = self.object.listing
        return reverse('auctions:listing_detail', args=[listing.id])

class BidCreateView(LoginRequiredMixin, View):
    login_url = '/login?next={{request.path}}'
    def post(self, request, pk) :
        f = get_object_or_404(Listing, id=pk)
        bid = Bid(amount=request.POST['bid'], owner=request.user, listing=f)
        bid.save()
        return redirect(reverse('auctions:listing_detail', args=[pk]))

@method_decorator(csrf_exempt, name="dispatch")
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        l = get_object_or_404(Listing, id=pk)
        fav = Favorite(user=request.user, listing=l)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name="dispatch")
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        l = get_object_or_404(Listing, id=pk)
        try:
            fav = Favorite.objects.get(user=request.user, listing=l).delete()
        except Favorite.DoesNotExist as e:
            pass

        return HttpResponse()

class CategoryListView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
