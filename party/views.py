from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from party.models import Post, Comment
from django.contrib.auth.decorators import login_required
from party.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.http import Http404
from braces.views import SelectRelatedMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
User = get_user_model()


# class PostListView(SelectRelatedMixin,ListView):
#     template_name = 'party/home.html'
#     model = Post
#     context_object_name = 'kuierlist'
#     select_related = ['user']

#     def get_queryset(self):
#         return Post.objects.order_by('-date')

# is_private = request.POST.get('is_private', False);

def post_list(request):
        polls = Post.objects.order_by('-date')
        search_term=''
        country_term=''

        if 'country' and 'search' in request.GET:
            try:
                search_term = request.GET['search']
                country_term = request.GET['country']
                polls = Post.objects.filter(title__icontains=search_term,color__icontains=country_term)
                get_dict_copy = request.GET.copy()
                params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
                context = {'kuierlist': polls, 'params': params, 'search_term': search_term}
                return render(request, 'party/home.html', context)
            except MultiValueDictKeyError:
                pass

            # if request.GET.get('country',False) != False and request.GET.get('search',False) != False:
            #         search_term = request.GET['search']
            #         country_term = request.GET['country']
            #         polls = Post.objects.filter(title__icontains=search_term,color__icontains=country_term)

        if 'country' in request.GET:
            search_term = request.GET['country']
            polls = Post.objects.filter(color__icontains=search_term)

        if 'date' in request.GET:
            polls = Post.objects.order_by('-date')

        if 'num_votes' in request.GET:
            polls = Post.objects.annotate(Count('vote')).order_by('-vote__count')

        if 'search' in request.GET:
            search_term = request.GET['search']
            polls = Post.objects.filter(Q(keyword__icontains=search_term) | Q(title__icontains=search_term))

        get_dict_copy = request.GET.copy()
        params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

        context = {'kuierlist': polls, 'params': params, 'search_term': search_term}
        return render(request, 'party/home.html', context)

class UserPosts(ListView):
    context_object_name = 'kuierlist'
    model = Post
    template_name = 'party/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('party').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.party.all()    
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context

class PostDetailView(SelectRelatedMixin,DetailView):
    model = Post
    template_name = 'party/post_detail.html'
    context_object_name = 'details'
    selectrelated = ['user']

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return get_object_or_404(Post,pk=id_)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class PostCreateView(LoginRequiredMixin,SelectRelatedMixin,CreateView):
    form_class = PostForm
    model = Post
    success_url = reverse_lazy("party:party")

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,DeleteView):
    model = Post
    select_related = ['user']
    success_url = reverse_lazy("party:party")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

class aboutTemplateView(TemplateView):
    template_name = 'party/about.html'

# def search(request):
#     template = 'party/post_list.html'

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('party:partydetail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'party/comment_form.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('party:partydetail', pk=post_pk)

def comment_display(request):
    comments = Comment.objects.all()
    context = {'commentlist':comments}
    return render(request,'party/post_detail.html',context)


# class CommentListView(SelectRelatedMixin,ListView):
#     template_name = 'party/post_detail.html'
#     model = Comment
#     context_object_name = 'commentlist'

#     def get_queryset(self):
#         return Comment.objects.order_by('-date')
