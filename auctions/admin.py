from django.contrib import admin
from auctions.models import Listing, Comment, Bid, Favorite, Category

# Register your models here.
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Favorite)
admin.site.register(Category)