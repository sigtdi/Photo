from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Post, Like, CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm, CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author.id != request.user.id:
        return redirect('hehe')
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author.id != request.user.id:
        return redirect('hehe')
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author.id != request.user.id:
        return redirect('hehe')
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def hehe(request):
    return render(request, 'blog/hehe.html')


def user_profile(request, pk):
    current_user = get_object_or_404(CustomUser, pk=pk)
    user = request.user
    return render(request, 'blog/user_profile.html', {'user': user, 'current_user': current_user})


def edit_profile(request, pk):
    user = request.user
    current_user = get_object_or_404(CustomUser, pk=pk)
    if current_user.id != user.id:
        return redirect('hehe')
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=pk)
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'blog/edit_profile.html', {'form': form})


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    likes = Like.objects.filter(post=post)
    return render(request, 'blog/post_detail.html', {'post': post, 'likes': likes})


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if not Like.objects.filter(post=post, user=request.user).exists():
        post.likes += 1
        post.save()
        Like.objects.create(post=post, user=request.user)
    else:
        post.likes -= 1
        post.save()
        Like.objects.filter(post=post, user=request.user).delete()
    return redirect('post_detail', pk=post.pk)
