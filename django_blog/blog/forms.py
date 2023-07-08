from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    name: forms.CharField = forms.CharField(max_length=25)
    email: forms.EmailField = forms.EmailField()
    to: forms.EmailField = forms.EmailField()
    comments: forms.CharField = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model: type = Comment
        fields: list[str] = ["name", "email", "body"]
