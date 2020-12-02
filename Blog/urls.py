from django.contrib import admin
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.splash, name='splash'),
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.SignUp.as_view(), name = 'signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('/home', views.home, name='home'),
    path('create/', views.create, name = 'create'),
    path('viewmypost/', views.viewmy, name = 'viewMy'),
    path('viewotherspost/<author_id>', views.viewothers, name='viewOthers'),
    path('delete/<post_id>', views.delete_post, name='delete'),
    path('like/<post_id>', views.like_post, name='like'),
    path('comment/<post_id>', views.comment, name='comment'),
    path('tag/<tag_id>', views.tag, name='viewTag')
]