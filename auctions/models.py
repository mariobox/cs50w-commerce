from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


class User(AbstractUser):
    # superuser: mario Rv$25
    pass

class Category(models.Model):
    """Model representing a listing category."""
    name = models.CharField(max_length=200, help_text='Enter a category (e.g. Books)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Listing(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    text = models.TextField()
    initial_bid = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Favorite', related_name='favorite_listings')
    image = models.URLField(max_length=200)
    active = models.BooleanField(default=True)
    # Category class has already been defined so we can specify the object above.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text='Select a category for this listing')
    # Shows up in the admin list
    def __str__(self):
        return self.title

class Favorite(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites_users')

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('listing', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.listing.title[:10])

class Comment(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

