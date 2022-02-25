from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views import generic
from groups.models import Group, GroupMember
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from posts.models import Post, Like

# Create your views here.
class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

    def get_context_data(self, **kwargs):
        context = super(SingleGroup, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        query = self.request.GET.get('q')
        if query:
            posts = Paginator(Post.objects.filter(Q(group=self.object) &
                                                 (Q(title__icontains=query) | Q(message__icontains=query))).order_by('created_at'), 3)
        else:
            posts = paginator = Paginator(Post.objects.filter(group=self.object).order_by('created_at'), 3)  # will show 3 items in one page
        posts_for_likes = Post.objects.filter(group=self.object)
        liked = []
        not_liked = []
        for post in posts_for_likes:
            if Like.objects.filter(post=post, user=self.request.user).count() == 1:
                liked.append(post)
            else:
                not_liked.append(post)
        context['liked'] = liked
        context['not_liked'] = not_liked
        context['paginator'] = posts
        context['is_group'] = True
        context['posts'] = posts.get_page(page)

        return context

class ListGroups(generic.ListView):
    model = Group

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        if query:
            object_list = Group.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            object_list = Group.objects.all()
        return object_list

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user = self.request.user,
                group__slug = self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have successfully left the group!')

        return super().get(request, *args, **kwargs)
