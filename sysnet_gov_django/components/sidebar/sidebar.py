from django_components import component

@component.register("gov_sidebar")
class GovSidebar(component.Component):
    template_name = "sidebar/sidebar.html"

    def get_context_data(self, menu_items=None, **kwargs):
        return {
            "menu_items": menu_items or [],
            "attrs": kwargs
        }
