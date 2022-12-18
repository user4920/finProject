from django.shortcuts import render, redirect
from .models import Post, Category, Genre
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.
class PostList(ListView):
  model = Post
  paginate_by = 6
  ordering = '-pk'

  def get_context_data(self, *, object_list=None, **kwargs):
    context = super(PostList, self).get_context_data()

    page = context['page_obj']
    paginator = page.paginator
    pagelist = paginator.get_elided_page_range(page.number, on_each_side=2, on_ends=1)
    context['pagelist'] = pagelist

    context['categories'] = Category.objects.all()
    context['no_category_post_count'] = Post.objects.filter(category=None).count()
    return context

class PostDetail(DetailView):
  model = Post

  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data()
    return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Post
  fields = ['title', 'subtitle', 'hook_text', 'head_image', 'price', 'studio', 'category', 'genre', 'created_at', 'content']

  def test_func(self):
    return self.request.user.is_superuser or self.request.user.is_staff

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
      form.instance.author = current_user
      return super(PostCreate, self).form_valid(form)
    else:
      return redirect('/mall/')

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