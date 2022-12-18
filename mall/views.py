from django.shortcuts import render
from .models import Post, Category, Genre
from django.views.generic import ListView, DetailView


# Create your views here.
class PostList(ListView):
  model = Post
  ordering = '-pk'

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(PostList, self).get_context_data()

    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Post.objects.filter(category=None).count()
    return context

class PostDetail(DetailView):
  model = Post

  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data()
    return context

class CategoryPage(PostList):
  def get_queryset(self):
    slug = self.kwargs['slug']

    if slug == 'no_category':
      post_list = Post.objects.filter(category=None)
    else:
      category = Category.objects.get(slug=slug)
      post_list = Post.objects.filter(category=category)

    return post_list

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(CategoryPage, self).get_context_data()

    slug = self.kwargs['slug']
    if slug == 'no_category':
      category = '미분류'
    else:
      category = Category.objects.get(slug=slug)

    context['category'] = category
    return context

class GenrePage(PostList):

  def get_queryset(self):
    slug = self.kwargs['slug']
    genre = Genre.objects.get(slug=slug)
    post_list = genre.post_set.all()

    return post_list

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(GenrePage, self).get_context_data()

    slug = self.kwargs['slug']
    genre = Genre.objects.get(slug=slug)

    context['genre'] = genre
    return context