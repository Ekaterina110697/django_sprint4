from django import forms

from .models import Post, User, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'created_at')
        widgets = {
            'pub_date': forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                            attrs={"type": "datetime-local"}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
