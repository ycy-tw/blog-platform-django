from django import forms
from django.core.exceptions import ValidationError
from .models import Comment, Post
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'comment_body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'readonly': True}),
            'comment_body': forms.Textarea(
                attrs={
                    'required': True,
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': _('Leave your comment.')}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'id': 'search',
                'class': 'form-control',
                'placeholder': _('Search'),
            }
        )
    )


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'body', 'cover_image', 'description', 'tags', 'status', 'title'
        ]
        widgets = {
            'body': CKEditor5Widget(
                config_name='extends',
                attrs={'placeholder': _('Write Something...')},
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'minlength': '10',
                    'required': False,
                    'style': 'height:200px; resize:none',
                }
            ),
            'cover_image': forms.FileInput(attrs={'class': '', 'style': 'visibility:hidden;'}),
            'tags': forms.TextInput(
                attrs={
                    'class': 'form-control tagsinput',
                    'autocomplete': 'off',
                    'data-role': 'tagsinput',
                    'required': False,
                },
            ),
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'required': False,
                }
            ),
            'status': forms.Select(attrs={'class': 'form-control', 'autocomplete': 'off', }),
        }
        labels = {
            'description': _('Description'),
            'cover_image': _('Cover Image'),
            'tags': _('Tags'),
            'status': _('Status'),
            'title': _('Title'),
        }

        help_texts = {
            'description': _('Write some intro for article.'),
            'tags': _('Name a tag and press enter, up to five'),
        }

    def __init__(self, *args, **kwargs):

        # first call parent's constructor
        super(ArticleForm, self).__init__(*args, **kwargs)

        # there's a `fields` property now
        self.fields['description'].required = False
        self.fields['tags'].required = False
        self.fields['title'].required = False
