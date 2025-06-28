from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    """
    Form for sending an email with a link to a blog post.
    """
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    # Optional comments field
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
