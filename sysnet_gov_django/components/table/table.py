from django_components import component

@component.register("gov_data_table")
class GovDataTable(component.Component):
    template_name = "table/table.html"

    def get_context_data(self, headers, rows, hx_target=None, hx_url=None, **kwargs):
        return {
            "headers": headers,
            "rows": rows,
            "hx_target": hx_target,
            "hx_url": hx_url,
            "attrs": kwargs
        }
