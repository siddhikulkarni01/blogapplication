from django import forms
from .models import Profile, BlogPost, LikeUnlike

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )

class LikeUnlikeForm(forms.ModelForm):
    class Meta:
        model = LikeUnlike
        fields = ('user_id', 'post_id', 'is_like')

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'image', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of the Blog'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Copy the title with no space and a hyphen in between'}),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content of the Blog'}),
            'status': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Status of the Blog'}),
        }