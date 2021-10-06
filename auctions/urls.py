from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from . import views

app_name='auctions'
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('', views.ListingListView.as_view(), name="index"),
    path('listing/<int:pk>', views.ListingDetailView.as_view(), name='listing_detail'),
    path('listing/create', views.ListingCreateView.as_view(success_url=reverse_lazy('auctions:index')), name='listing_create'),
    path('listing/<int:pk>/update',
        views.ListingUpdateView.as_view(success_url=reverse_lazy('auctions:index')), name='listing_update'),
    path('listing/<int:pk>/delete',
        views.ListingDeleteView.as_view(success_url=reverse_lazy('auctions:index')), name='listing_delete'),
    path('listing/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='listing_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('auctions:listing_detail')), name='listing_comment_delete'),
    path('listing/<int:pk>/bid',
        views.BidCreateView.as_view(), name='listing_bid_create'),  
    path('listing/<int:pk>/favorite', 
        views.AddFavoriteView.as_view(), name='listing_favorite'),
    path('listing/<int:pk>/unfavorite', 
        views.DeleteFavoriteView.as_view(), name='listing_unfavorite'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorites'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),
    path('accounts/login', RedirectView.as_view(url='login/', permanent=True)),          
]
