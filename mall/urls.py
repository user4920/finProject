from django.urls import path
from . import views

urlpatterns = [ # IP주소/mall/
  path('', views.PostList.as_view()),
  path('<int:pk>/', views.PostDetail.as_view()),
]