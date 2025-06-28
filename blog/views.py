from django.views.generic import ListView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from gc import get_objects
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag

#
# # Create a class-based view for listing blog posts
# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     queryset = Post.published.all() # Use the custom manager to get published posts
#     context_object_name = 'posts' # Name of the context variable to be used in the template
#     paginate_by = 3  # Show 3 posts per page
#     template_name = 'blog/post/list.html'  # Specify your template name here
#
#     # The (ListView) class automatically provides a (page_obj) context variable
#     # when pagination is enabled (via the paginate_by attribute).
#     # This variable represents the current page of paginated objects
#     # and is used in the template for rendering pagination controls.

# Create a post-list view function
def post_list(request, tag_slug=None):
    """
    View function to display a list of published blog posts.
    """
    # Retrieve all published posts using the custom manager
    blog_posts_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Instantiate Pagination class with 3 posts objects per page
    paginator = Paginator(blog_posts_list, 3)  # Show 3 posts per page

    # Retrieve the page GET HTTP parameter and store it in page_number variable
    # This parameter contains the page number to be displayed
    # If no page number is in GET, default to the first page (1)
    page_number = request.GET.get('page', 1)  # Get the page number from the query parameters

    try:
        # Get the page for the desired page number by calling page() method of the Paginator
        posts = paginator.page(page_number)  # Get the posts for the current page
        # posts will be a Page object containing the posts for the current page -> exposed to the template
    except PageNotAnInteger:
        # If the page number is not an integer, return the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If the page number is out of range, return the last page
        posts = paginator.page(paginator.num_pages) # num_pages method returns the total number of pages

    # render the template with the posts-context
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts, 'tag': tag}
    )

# Create a post-detail view function
def post_detail(request, year, month, day, slug):
    """
    View function to display the details of a specific blog post.
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=slug, # slug parameter passed in from the URL path (slug:post),
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    # Add comments to post detail view
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
         }
    )

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )

@require_POST # Ensure this view only accepts HTTP POST methods requests
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form, # form is the CommentForm instance
            'comment': comment
        }
    )