from django_components import component

@component.register("gov_card")
class GovCard(component.Component):
    template_name = "card/card.html"

    def get_context_data(self, title=None, **kwargs):
        return {
            "title": title,
            "attrs": kwargs
        }
