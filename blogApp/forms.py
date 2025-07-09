from django import forms

from blogApp.models import PostComment


class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['name' , 'comment']

