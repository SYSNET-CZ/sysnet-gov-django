from django_components import component

@component.register("gov_field")
class GovField(component.Component):
    template_name = "field/field.html"

    def get_context_data(self, label, name, help_text=None, errors=None, required=False, **kwargs):
        return {
            "label": label,
            "name": name,
            "help_text": help_text,
            "errors": errors,
            "required": required,
            "attrs": kwargs
        }
