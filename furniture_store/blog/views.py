from django.shortcuts import render, get_object_or_404
from .models import Post, Tag

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'apps/blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'apps/blog/post_detail.html', {'post': post})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, is_published=True).order_by('-created_at')
    return render(request, 'apps/blog/tag_detail.html', {'tag': tag, 'posts': posts})