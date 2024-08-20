from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count

def home(request):                        
    forums = Category.objects.all()

    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    num_categories = Category.objects.all().count()
    last_post = Post.objects.latest("date")


    context = {
        "forums": forums,
        "num_posts": num_posts,
        "num_users": num_users,
        "num_categories": num_categories,
        "last_post": last_post,
    }
    return render(request, 'home.html', context)


def posts(request, slug=None): 

    if slug:
        category = get_object_or_404(Category, slug=slug)
        posts = Post.objects.filter(categories=category).annotate(num_comments_count=Count('comments')).order_by('-num_comments_count')

        # posts = Post.objects.filter(categories=category).order_by('-num_comments')
        paginator = Paginator(posts, 5)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {'category': category, 'posts': posts}
    else:
        # posts = Post.objects.all().order_by('-num_comments')
        posts = Post.objects.all().annotate(num_comments_count=Count('comments')).order_by('-num_comments_count')

        paginator = Paginator(posts, 5)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context = {'posts': posts}

    return render(request, 'posts.html', context)

def details(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
    else:
        return redirect('signin')
    if "comment-form" in request.POST:
        comment = request.POST.get("comment1")        
        new_comment, date_created = Comment.objects.get_or_create(user=author, content=comment)
        post.comments.add(new_comment.id)
    elif "reply-form" in request.POST:
            reply = request.POST.get("reply1")
            if reply:  # Only create a reply if it's not empty
                print(f"Reply content: {reply}")  # Debugging line
                comment_id = request.POST.get("comment-id")
                comment = Comment.objects.get(id=comment_id)

                new_reply, date_created = Reply.objects.get_or_create(user=author, content=reply)
                comment.replies.add(new_reply.id)
    
    if slug:
        context = {"post": post,
                   "author": author}
    else:
        context = {}  # Or provide some default context if needed
    update_views(request, post)
    return render(request, 'details.html', context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        author = Author.objects.get(user=request.user)
        new_post = form.save(commit=False)
        new_post.user = author
        author.num_posts += 1
        author.save()
        new_post.save()
        form.save_m2m()  # Save the many-to-many data for the form
        return redirect("home")
    context = {
        "form": form,
        "title": "Create New Post"
    }
    return render(request, "create_post.html", context)


def latest_posts(request):
    posts = Post.objects.all().filter().order_by('-date')[:10]
    context = {
        "posts": posts,
        "title": "Last 10 Posts"
    }
    return render(request, "latest_posts.html", context)


def search_result(request):
    return render(request, "search.html")