# sysnet-gov-django

Django UI knihovna založená na **Gov.cz Design Systému (v4)**. 
Tato knihovna neimplementuje business logiku, ale poskytuje Django Template Tags a šablony pro rychlou tvorbu GDS compliant rozhraní přímo v Django šablonách (SSR).

Vychází z designových tokenů definovaných v [sysnet-gov-ui](../sysnet-gov-ui/).

## Instalace
```bash
pip install sysnet-gov-django
```

## Použití
V `settings.py`:
```python
INSTALLED_APPS = [
    ...,
    "django_components",
    "sysnet_gov_django",
]

# Pro django-components v settings.py
COMPONENTS = {
    "libraries": [
        "sysnet_gov_django.components.button.button",
        "sysnet_gov_django.components.card.card",
        "sysnet_gov_django.components.form.layout",
        "sysnet_gov_django.components.sidebar.sidebar",
        "sysnet_gov_django.components.field.field",
        "sysnet_gov_django.components.table.table",
        "sysnet_gov_django.components.select.select",
        "sysnet_gov_django.components.breadcrumbs.breadcrumbs",
    ],
}
```

V šabloně:
```html
{% load gov_tags %}

{% gov_alert text="Systém je v údržbě" type="warning" title="Pozor" %}
{% gov_button text="Uložit data" type="primary" %}
```

## Obsah
- `sysnet_gov_django/templatetags/` — Template tagy mapované na GDS komponenty.
- `sysnet_gov_django/templates/gov_django/` — HTML šablony komponent.
- `sysnet_gov_django/static/gov_django/` — CSS/JS (vygenerované ze sysnet-gov-ui).
