from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.core.paginator import Paginator
from braces.views import SelectRelatedMixin
from django.http import Http404
from groups.models import Group
from accounts.models import Profile
from . import models
from . import forms

# Create your views here.
class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', 'group')

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)

        #paginator code
        page = self.request.GET.get('page')
        posts = paginator = Paginator(models.Post.objects.all().order_by('-created_at'), 3)  # will show 3 items in one page
        context['paginator'] = posts
        context['posts'] = posts.get_page(page)

        #display all groups and the groups of the authenticated user's
        if self.request.user.is_authenticated:
            context['user_groups'] = models.Group.objects.filter(members__in=[self.request.user])
        context['all_groups'] = models.Group.objects.all()

        return context


class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    paginate_by = 3

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_groups'] = models.Group.objects.filter(members__in=[self.request.user])
        context['post_user'] = self.post_user
        context['form'] = forms.ProfileForm(instance=Profile.objects.get(user=self.request.user))
        return context

class AvatarForm(generic.FormView):
    form_class = forms.ProfileForm
    model = Profile

    # def form_valid(self, form):
    #     # self.object = form.save(commit=False)
    #     # self.object.user = self.request.user
    #     # self.object.save()
    #
    #     print(self.)
    #
    #     return super().form_valid(form)

    def get_form(self, form_class=None):
        """
        Check if the user already has a profile. If so, then show
        the form populated with those details, to let user change them.
        """
        try:
            if form_class is None:
                form_class = self.get_form_class()
            profile  = Profile.objects.get(user=self.request.user)
            print(profile.avatar)
            return form_class(instance=profile, **self.get_form_kwargs())
        except Profile.DoesNotExist:
            return form_class(**self.get_form_kwargs())


    def get_success_url(self):
        return reverse('posts:for_user', kwargs={'username':self.request.user})

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', 'group')

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form_comment'] = forms.CommentForm
        context['form_reply'] = forms.CommentForm
        context['is_detail'] = True
        context['is_liked'] = models.Like.objects.filter(user=self.request.user, post=self.object).count() == 1
        if context['is_liked'] == 1:
            context['like'] = models.Like.objects.get(user=self.request.user, post=self.object)
        context['is_group'] = True

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CommentForm(generic.FormView):
    form_class = forms.CommentForm
    model = models.Comment

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = models.Post.objects.get(pk=self.kwargs['pk'])
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:single', kwargs={'username':self.request.user, 'pk':self.kwargs['pk']})

class ReplyForm(generic.FormView):
    form_class = forms.CommentForm
    model = models.Comment

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = models.Post.objects.get(pk=self.kwargs['post_pk'])
        self.object.parent_comment = models.Comment.objects.get(pk=self.kwargs['comment_pk'])
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:single', kwargs={'username':self.request.user, 'pk':self.kwargs['post_pk']})

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('title', 'message', 'image')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.group = Group.objects.get(slug=self.kwargs['group_slug'])
        self.object.save()

        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_context_data(self, **kwargs):
        context = super(DeletePost, self).get_context_data(**kwargs)
        context['is_delete_view'] = True

        return context


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)

@login_required
def add_like_to_post(request, username, pk):
    post = get_object_or_404(models.Post, pk=pk)
    user = get_object_or_404(User, id=request.user.id)

    like = models.Like(post=post, user=user)
    like.save()

    return redirect('posts:single', username=post.user.username, pk=pk)

@login_required
def add_like_to_post_group_view(request, username, pk, page):
    post = get_object_or_404(models.Post, pk=pk)
    user = get_object_or_404(User, id=request.user.id)

    like = models.Like(post=post, user=user)
    like.save()

    return redirect(reverse('groups:single', kwargs={'slug':post.group.slug}) + "?page=" + page)

@login_required
def remove_like_from_post(request, username, post_pk):
    post = get_object_or_404(models.Post, pk=post_pk)
    like = models.Like.objects.get(user=request.user, post=post)

    models.Like.objects.filter(pk=like.pk).delete()

    return redirect('posts:single', username=post.user.username, pk=post.pk)

@login_required
def remove_like_from_post_group_view(request, username, post_pk, page):
    post = get_object_or_404(models.Post, pk=post_pk)
    like = models.Like.objects.get(user=request.user, post=post)

    models.Like.objects.filter(pk=like.pk).delete()

    return redirect(reverse('groups:single', kwargs={'slug':post.group.slug}) + "?page=" + page)

@login_required
def update_profile_picture(request, username):
    profile = get_object_or_404(Profile, user=request.user)

    #delete previous profile picture from memory
    if profile.avatar and profile.avatar != 'profile_pics/default.jpg':
        profile.avatar.delete()

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('posts:for_user', username=request.user.username)

    return redirect('posts:for_user', username=request.user.username)
