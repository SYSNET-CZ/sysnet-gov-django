from django import forms

class GovInputWidget(forms.TextInput):
    template_name = "gov_django/widgets/input.html"
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'gov-form-control'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

class GovSelectWidget(forms.Select):
    template_name = "gov_django/widgets/select.html"

class GovCheckboxWidget(forms.CheckboxInput):
    template_name = "gov_django/widgets/checkbox.html"

class GovFormMixin:
    """Mixin přidávající GDS stylování k Django formulářům."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                field.widget.attrs.update({'class': 'gov-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'gov-select'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'gov-checkbox'})
            
            if field.required:
                field.widget.attrs.update({'aria-required': 'true'})
