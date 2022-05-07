from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        """
        Remove auto-generated label, add placeholder and add a 
        class to content field
        """
        super().__init__(*args, **kwargs)
        self.fields['content'].label = False
        self.fields['content'].widget.attrs['placeholder'] = (
            'Please write your review here...'
        )
        self.fields['content'].widget.attrs['rows'] = 5
        self.fields['content'].widget.attrs['class'] = 'review-form-input'
