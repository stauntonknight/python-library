from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import CreateView 
from users.models import User
from django.core.urlresolvers import reverse

class ListUserView(ListView):
    model = User
    template_name = 'user_list.html'

class CreateUserView(CreateView):
    model = User
    template_name = 'edit_user.html'

    def get_success_url(self):
        return reverse('users-list')


# Create your views here.
