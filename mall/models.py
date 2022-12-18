from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 제조사
class Studio(models.Model):
  # 추가 필드 - 회사 이름
  name = models.CharField(max_length=30, unique=True)
  slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

  # 주소
  address = models.CharField(max_length=100, unique=True)

  # 연락처
  email = models.CharField(max_length=30, unique=True, null=True, blank=True)

  # 추가 필드 - 회사 소개
  content = models.TextField(blank=True)

  def __str__(self):
    return self.name

# 카테고리
class Category(models.Model):
  name = models.CharField(max_length=30, unique=True)
  slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/mall/category/{self.slug}/'

  class Meta:
    verbose_name_plural = 'Categories'

# 장르
class Genre(models.Model):
  name = models.CharField(max_length=30, unique=True)
  slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/mall/genre/{self.slug}/'

# 상품 모델
class Post(models.Model):
  # 1. 상품명
  title = models.CharField(max_length=30)

  # 1-1. 추가필드 - subtitle
  subtitle = models.CharField(max_length=50, blank=True)

  # 2. 간단한 설명
  hook_text = models.CharField(max_length=300, blank=True)

  # 3. 상품 이미지
  head_image = models.ImageField(upload_to='mall/images/%Y/%m/%d/')

  # 4. 상품 가격
  price = models.IntegerField()

  # 5. 제조사(개발자) - 해당 제조사의 상품이 있을 경우, 제조사 삭제 불가
  studio = models.ForeignKey(Studio, on_delete=models.PROTECT)

  # 6. 카테고리 - 삭제 시, null 값 지정
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

  # 7. 다대다 관계 필드 - 장르
  genre = models.ManyToManyField(Genre, blank=True)

  # 8. 추가 필드 - 등록일
  uploaded_at = models.DateField(auto_now_add=True)

  # 8-1. 추가 필드 - 출시일
  created_at = models.DateField()

  # 9. 추가 필드 - 자세한 설명
  content = models.TextField()

  # 10. 작성자 - superuser 또는 staff
  author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

  def __str__(self):
    if self.subtitle:
      return f'[{self.pk}]{self.title}-{self.subtitle}::{self.studio}'
    else:
      return f'[{self.pk}]{self.title}::{self.studio}'

  def get_absolute_url(self):
    return f'/mall/{self.pk}/'

class Comment(models.Model):
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default="이름없음")
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.author}::{self.content}'

  def get_absolute_url(self):
    return f'{self.post.get_absolute_url()}#comment-{self.pk}'

  def get_avatar_url(self):
    if self.author.socialaccount_set.exists():
      return self.author.socialaccount_set.first().get_avatar_url()
    else:
      return 'https://dummyimage.com/50x50/ced4da/6c757d.jpg'