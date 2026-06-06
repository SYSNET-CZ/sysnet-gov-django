from django_components import component

@component.register("gov_footer")
class GovFooter(component.Component):
    template_name = "footer/footer.html"

    def get_context_data(self, **kwargs):
        return {
            "attrs": kwargs
        }
