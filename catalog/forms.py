from django import forms

from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    RESTRICTED_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
        'дёшево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = '__all__'

    def restrict_words(self, title):
        for word in self.RESTRICTED_WORDS:
            if word.lower() in title.lower():
                raise forms.ValidationError(f'Недопустимое слово "{word}"')

    def clean_name(self):
        cleaned_data = (self.cleaned_data.get('name'))
        self.restrict_words(cleaned_data)
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data.get('description')
        self.restrict_words(cleaned_data)
        return cleaned_data


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'
