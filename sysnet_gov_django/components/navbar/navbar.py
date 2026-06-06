from django_components import component

@component.register("gov_navbar")
class GovNavbar(component.Component):
    template_name = "navbar/navbar.html"

    def get_context_data(self, brand_name="Gov Project", menu_items=None, user=None, **kwargs):
        return {
            "brand_name": brand_name,
            "menu_items": menu_items or [],
            "user": user,
            "attrs": kwargs
        }
