from django_components import component

@component.register("gov_layout")
class GovLayout(component.Component):
    template_name = "form/layout.html" # Dočasně v form/ dokud neudělám layout/

    def get_context_data(self, page_title="Gov Project", **kwargs):
        return {
            "page_title": page_title,
        }
