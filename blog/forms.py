from django import forms
from blog.models import Post, Comments
from django.forms import ModelForm, Textarea


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'text',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = (
            'text',
        )
        widgets = {
            'text': Textarea(attrs={'rows': 4, 'cols': 40})
        }
