from django.shortcuts import render, get_list_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    context = {
        'posts': Post.objects.all(),
    }

    return render(request, 'blog/home.html', context)

# Class based views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        # user = get_list_or_404(User, username=self.kwargs.get('username'))
        user = User.objects.get(username=self.kwargs.get('username'))

        return Post.objects.all().order_by('-date_posted').filter(author=user)
        # return super().get_queryset().filter(author=user)
    



class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # override form and add author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # override form and add author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    # User owns the post they're trying to update
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    # User owns the post they're trying to update
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')