from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from blog.models import Post, Category


POSTS_PER_PAGE = 5


def index(request: HttpRequest) -> HttpResponse:
    template = 'blog/index.html'
    posts = (
        Post.published.get_posts_qs()
        .order_by('-created_at')[:POSTS_PER_PAGE])
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request: HttpRequest, id: int):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.base_filters(),
        pk=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    posts = get_list_or_404(
        Post.objects.base_filters()
        .filter(
            category__title=category.title,
        )
    )
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, template, context)
