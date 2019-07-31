from .models import Post, Comment
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from .form import Postform
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def comment_write(request, post_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        content = request.POST.get('content')
        if not content:
            messages.info(request, "You dont write anything...")
            return redirect('/post/' + str(post_pk))

        Comment.objects.create(post_key=post, comment_contents=content)
        return redirect('/blog/post/'+str(post_pk))

def modify(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    return render(request, 'modify.html', {'post':post_detail})

def update(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    post.title = request.GET['title']
    post.content = request.GET['content']
    post.save()
    return redirect('/post/'+str(post.id))

def new(request):
    return render(request, 'new.html')

def create(request):
    post = Post()
    post.title = request.GET['title']
    post.content = request.GET['content']
    post.pub_date = timezone.datetime.now()
    post.save()
    return redirect('/blog/post/'+str(post.id))

def delete1(request, comment_id, post_id):
    comment = get_object_or_404(Comment , pk = comment_id )
    comment.delete()
    return redirect('/blog/post/'+str(post_id))


def delete(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    post.delete()
    return redirect('index')

@login_required
def index(request):
    posts = Post.objects.all().order_by('-id')

    return render(request, 'index.html', {'posts_show':posts})

def detail(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.get_username())
        return render(request, 'detail.html', {'post':post_detail, 'user':user})
    else:
        return render(request, 'detail.html', {'post':post_detail})
        
def newpost(request):
    if request.method == 'POST':
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(username=request.user.get_username())
            post.pub_date = timezone.now()
            post.save()
            return redirect('index')
    else:
        form = Postform()
        return render(request,'newpost.html',{'form':form})

def updatemodify(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = Postform(request.POST, request.FILES)
        if form.is_valid():
            post.title = form.cleaned_data['title']   
            post.content = form.cleaned_data['content']
            post.save()
            return redirect('/blog/post/' +str(post_id))
    else:
        form= Postform(instance=post)
        return render(request,'modify.html',{'form':form})

@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_like, post_like_created = post.like_set.get_or_create(user=request.user)

    if not post_like_created:
        post_like.delete()
        return redirect('/blog/post/'+str(post.id))
    return redirect('/blog/post/'+str(post.id))