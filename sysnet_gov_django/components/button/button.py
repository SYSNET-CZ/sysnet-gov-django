from django_components import component

@component.register("gov_button")
class GovButton(component.Component):
    template_name = "button/button.html"

    def get_context_data(self, text, type="primary", size="md", disabled=False, **kwargs):
        return {
            "text": text,
            "type": type,
            "size": size,
            "disabled": disabled,
            "attrs": kwargs
        }
