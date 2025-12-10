from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed, JsonResponse, HttpResponseRedirect
from django.views import View
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.urls import reverse
import sys

from .models import Post
    
def post_list(request):
    """Отображение списка всех постов"""
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'app/post_list.html', {'posts': posts})

def post_detail(request, pk):
    """Отображение одного поста"""
    post = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, 'app/post_detail.html', {'post': post})

def redirect_home(request):
    """Редирект на главную страницу"""
    return redirect('post_list')

def redirect_to_post(request, pk):
    """Редирект на конкретный пост"""
    return redirect('post_detail', pk=pk)
