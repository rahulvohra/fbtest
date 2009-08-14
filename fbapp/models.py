from django.db import models
from django import forms

# get_facebook_client lets us get the current Facebook object
# from outside of a view, which lets us have cleaner code
from facebook.djangofb import get_facebook_client

class UserManager(models.Manager):
    """Custom manager for a Facebook User."""
    
    def get_current(self):
        """Gets a User object for the logged-in Facebook user."""
        facebook = get_facebook_client()
        user, created = self.get_or_create(id=int(facebook.uid))
        if created:
            # we could do some custom actions for new users here...
            pass
        return user

class User(models.Model):
    """A simple User model for Facebook users."""

    # We use the user's UID as the primary key in our database.
    id = models.IntegerField(primary_key=True)

    # Add the custom manager
    objects = UserManager()

    def __unicode__(self):
        return str(self.id)
        
class Idea(models.Model):
    """A model which represents an Idea"""
    
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User)
    
class IdeaForm(forms.ModelForm):
    posted = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Idea
        exclude = ['user']