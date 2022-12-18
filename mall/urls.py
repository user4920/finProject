from django.urls import path
from . import views

urlpatterns = [ # IP주소/mall/
  path('', views.PostList.as_view()),
  path('<int:pk>/', views.PostDetail.as_view()),
  path('category/<str:slug>/', views.CategoryPage.as_view()),
  path('genre/<str:slug>/', views.GenrePage.as_view()),

  path('create_post/', views.PostCreate.as_view()),
  path('update_post/<int:pk>/', views.PostUpdate.as_view()),

  path('<int:pk>/new_comment/', views.new_comment),
  path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
  path('delete_comment/<int:pk>/', views.delete_comment),
]