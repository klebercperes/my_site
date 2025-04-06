from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            "text": "Your Comment"
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'What do you think about this post?'})
        }
    