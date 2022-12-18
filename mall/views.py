from django.shortcuts import render, redirect
from .models import Post, Category, Genre, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm

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
    context['comment_form'] = CommentForm
    return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
  model = Post
  fields = ['title', 'subtitle', 'hook_text', 'head_image', 'price', 'studio', 'category', 'created_at', 'content']

  def test_func(self):
    return self.request.user.is_superuser or self.request.user.is_staff

  def form_valid(self, form):
    current_user = self.request.user
    if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
      form.instance.author = current_user
      response = super(PostCreate, self).form_valid(form)

      genre_str = self.request.POST.get('genre_str')
      if genre_str:
        genre_str = genre_str.strip() #공백제거
        genre_str = genre_str.replace(',', ';') #쉼표->세미콜론
        genre_list = genre_str.split(';')

        for g in genre_list:
          g = g.strip()
          genre, is_genre_created = Genre.objects.get_or_create(name=g) #값이 있으면 가져오고, 없으면 생성
          if is_genre_created:
            genre.slug = slugify(g, allow_unicode=True)
            genre.save()
          self.object.genre.add(genre)

      return response

    else:
      return redirect('/mall/')

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ['title', 'subtitle', 'hook_text', 'head_image', 'price', 'studio', 'category', 'created_at', 'content']

  template_name = 'mall/post_update_form.html'

  def form_valid(self, form):
    response = super(PostUpdate, self).form_valid(form)
    self.object.genre.clear()

    genre_str = self.request.POST.get('genre_str')
    if genre_str:
      genre_str = genre_str.strip()  # 공백제거
      genre_str = genre_str.replace(',', ';')  # 쉼표->세미콜론
      genre_list = genre_str.split(';')

      for g in genre_list:
        g = g.strip()
        genre, is_genre_created = Genre.objects.get_or_create(name=g)  # 값이 있으면 가져오고, 없으면 생성
        if is_genre_created:
          genre.slug = slugify(g, allow_unicode=True)
          genre.save()
        self.object.genre.add(genre)

    return response

  def get_context_data(self, **kwargs):
    context = super(PostUpdate, self).get_context_data()
    if self.object.genre.exists():
      genre_str_list = list()
      for g in self.object.genre.all():
        genre_str_list.append(g.name)
      context['genre_str_default'] = ';'.join(genre_str_list)
    return context

class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  form_class = CommentForm

  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated and request.user == self.get_object().author:
      return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
    else:
      raise PermissionDenied

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