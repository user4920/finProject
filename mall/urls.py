from django.urls import path
from . import views

urlpatterns = [ # IP주소/mall/
  path('', views.PostList.as_view()),
  path('<int:pk>/', views.PostDetail.as_view()),
  path('category/<str:slug>/', views.CategoryPage.as_view()),
  path('genre/<str:slug>/', views.GenrePage.as_view()),
  path('create_post/', views.PostCreate.as_view()),
]