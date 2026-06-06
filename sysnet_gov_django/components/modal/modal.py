from django_components import component

@component.register("gov_modal")
class GovModal(component.Component):
    template_name = "modal/modal.html"

    def get_context_data(self, id, title=None, size="md", hx_url=None, **kwargs):
        return {
            "id": id,
            "title": title,
            "size": size,
            "hx_url": hx_url,
            "attrs": kwargs
        }
