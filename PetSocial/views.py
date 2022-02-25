from django.views.generic import TemplateView
from posts.models import Post, Like
from django.db.models import Count

class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        posts2 = Post.objects.filter(image__isnull=False).order_by('-created_at')[:3]
        posts = Post.objects.filter(image__isnull=False).annotate(num_likes=Count('post_likes')).order_by('-num_likes')
        context['posts'] = posts[:3]

        return context

class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'
