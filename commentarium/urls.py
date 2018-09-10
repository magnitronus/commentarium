"""commentarium URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from comments.views import CommentsViewSet
from entities.views import PostsViewSet, UserPageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'comments', CommentsViewSet, base_name='comments')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'posts', PostsViewSet, base_name='posts')
router.register(r'userpages', UserPageViewSet, base_name='userpages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='index.html')),
]
