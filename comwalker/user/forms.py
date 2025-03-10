# user/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review  # Use the Review model
        fields = ['rating', 'comment', 'image']  # Include only the rating and comment fields in the form
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),  # Add CSS classes for styling
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

from django import forms
from .models import CommunityPost

class CommunityPostForm(forms.ModelForm):
    class Meta:
        model = CommunityPost
        fields = ['product_name', 'description', 'image']
