from django import forms
from posts.models import Comment
from accounts.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ['text',]
        labels = {
            'text':'Write Your comment content here:'
        }

class ProfileForm(forms.ModelForm):

    class Meta():
        model = Profile
        fields = ['avatar']
        labels = {
            'avatar':''
        }

    # def get_form(self, request, form_class=None):
    #     """
    #     Check if the user already has a profile. If so, then show
    #     the form populated with those details, to let user change them.
    #     """
    #     try:
    #         if form_class is None:
    #             form_class = self.get_form_class()
    #         profile  = Profile.objects.get(user=self.request.user)
    #         print(profile.avatar)
    #         return form_class(instance=profile, **self.get_form_kwargs())
    #     except Profile.DoesNotExist:
    #         return form_class(**self.get_form_kwargs())
