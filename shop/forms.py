from django import forms
from .models import Review, Product, Type


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


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        types = Type.objects.all()
        friendly_names = [(t.id, t.get_friendly_name()) for t in types]

        self.fields['type'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'add-product-input'
