from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.views.generic import list_detail
from django.views.generic import create_update
from django.shortcuts import render_to_response
#uncomment the following two lines and the one below
#if you dont want to use a decorator instead of the middleware
#from django.utils.decorators import decorator_from_middleware
#from facebook.djangofb import FacebookMiddleware

# Import the Django helpers
import facebook.djangofb as facebook

# The User model defined in models.py
from models import *

# We'll require login for our canvas page. This
# isn't necessarily a good idea, as we might want
# to let users see the page without granting our app
# access to their info. See the wiki for details on how
# to do this.
#@decorator_from_middleware(FacebookMiddleware)
@facebook.require_login()
def index(request):
    # Get the User object for the currently logged in user
    user = User.objects.get_current()

    # Check if we were POSTed the user's new language of choice
    # if 'language' in request.POST:
    #     user.language = request.POST['language'][:64]
    #     user.save()

    # ideas = Idea.objects.all()

    # User is guaranteed to be logged in, so pass canvas.fbml
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    # return direct_to_template(request, 'canvas.fbml', extra_context={'fbuser': user, 'ideas': ideas})
    return list_detail.object_list(
        request,
        queryset = Idea.objects.all(),
        template_name = "canvas.fbml",
        template_object_name = "idea",
        extra_context = {"fbuser": user},
    )

@facebook.require_login()
def new_idea(request):
    fb = request.facebook
    user = User.objects.get_current()

    if 'posted' in request.POST:
        form = IdeaForm(data=request.POST)
        if form.is_valid():
            idea = form.save(commit=False)    
            idea.user = user
            idea.save()
            return fb.redirect('http://apps.facebook.com/vohratest/ideas/')
    else:
        form = IdeaForm()
        
    return render_to_response('fbapp/idea_form.html',{"fbuser": user, 'form':form})

    

@facebook.require_login()
def ajax(request):
    return HttpResponse('hello world')
