from django_components import component

@component.register("gov_master_layout")
class GovMasterLayout(component.Component):
    template_name = "form/master.html"

    def get_context_data(self, page_title="Gov Project", brand_name=None, menu_items=None, user=None, sidebar_items=None, **kwargs):
        return {
            "page_title": page_title,
            "brand_name": brand_name or page_title,
            "menu_items": menu_items,
            "user": user,
            "sidebar_items": sidebar_items,
        }
