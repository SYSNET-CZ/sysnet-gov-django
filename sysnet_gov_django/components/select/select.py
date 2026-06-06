from django_components import component

@component.register("gov_select")
class GovSelect(component.Component):
    template_name = "select/select.html"

    def get_context_data(self, label, name, options, value=None, help_text=None, errors=None, required=False, **kwargs):
        return {
            "label": label,
            "name": name,
            "options": options,
            "value": value,
            "help_text": help_text,
            "errors": errors,
            "required": required,
            "attrs": kwargs
        }
