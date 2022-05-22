from django import forms
from .widgets import CustomClearableFileInput
from .models import Review, Product, Type, Brand, Flavour


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
        self.fields['content'].widget.attrs['id'] = 'review-form-content'


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        types = Type.objects.all()
        type_friendly_names = [
            (t.id, t.get_friendly_name()) for t in types
        ]
        type_friendly_names.insert(0, (u'', u''))

        brands = Brand.objects.all()
        brand_friendly_names = [
            (b.id, b.get_friendly_name()) for b in brands
        ]
        brand_friendly_names.insert(0, (u'', u''))

        flavours = Flavour.objects.all()
        flavour_friendly_names = [
            (f.id, f.get_friendly_name()) for f in flavours
        ]
        flavour_friendly_names.insert(0, (u'', u''))

        self.fields['type'].choices = type_friendly_names
        self.fields['brand'].choices = brand_friendly_names
        self.fields['flavour'].choices = flavour_friendly_names
        self.fields['description'].widget.attrs['rows'] = 5
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'add-product-input'
