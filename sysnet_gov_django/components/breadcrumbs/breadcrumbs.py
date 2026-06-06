from django_components import component

@component.register("gov_breadcrumbs")
class GovBreadcrumbs(component.Component):
    template_name = "breadcrumbs/breadcrumbs.html"

    def get_context_data(self, items, **kwargs):
        return {
            "items": items,
            "attrs": kwargs
        }
