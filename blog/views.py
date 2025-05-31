from gc import get_objects
from django.shortcuts import render, get_object_or_404
from .models import Post

# Create a post-list view function
def post_list(request):
    """
    View function to display a list of published blog posts.
    """
    posts = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )

# Create a post-detail view function
def post_detail(request, id):
    """
    View function to display the details of a specific blog post.
    """
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED,
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
