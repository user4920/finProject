from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

# Create your views here.
class PostList(ListView):
  model = Post
  ordering = '-pk'

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(PostList, self).get_context_data()
    return context