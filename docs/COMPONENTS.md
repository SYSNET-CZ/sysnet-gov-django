# sysnet-gov-django: Dokumentace UI knihovny

Knihovna implementuje **Gov.cz Design System (v4)** pro prostředí **Django SSR** pomocí frameworku `django-components`.

## Architektura
Projekt je postaven na komponentovém přístupu:
- Každý prvek je zapouzdřen do třídy `Component` pod `sysnet_gov_django/components/`.
- Podpora **slotů** umožňuje vkládání libovolného obsahu do komponent.
- Integrace s **Django Forms** skrze `GovFormMixin`.

## Komponenty

### 1. GovLayout (`{% component "gov_layout" %}`)
Základní master template. Definujte v něm strukturu celé aplikace.
**Sloty:** `head`, `header`, `content`, `footer`, `scripts`.

### 2. GovSidebar (`{% component "gov_sidebar" %}`)
Postranní navigace se slotem pro libovolný obsah menu.
```html
{% component "gov_sidebar" menu_items=menu %}
    {% fill "content" %}
        <!-- Vlastní HTML menu v případě potřeby -->
    {% endfill %}
{% endcomponent %}
```

### 3. GovField (`{% component "gov_field" %}`)
Obal formulářového prvku s labelem, help textem a validací.
```html
{% component "gov_field" label="Jméno" name="first_name" required=True %}
    {% fill "input" %}
        <input type="text" name="first_name" id="id_first_name" class="gov-input">
    {% endfill %}
{% endcomponent %}
```

### 4. GovCard (`{% component "gov_card" %}`)
Strukturovaný box.
**Sloty:** `header_actions`, `content`, `footer`.

### 5. GovModal (`{% component "gov_modal" %}`)
GDS modální okno s podporou asynchronního načítání obsahu.
```html
{% component "gov_modal" id="myModal" title="Detail záznamu" %}
    {% fill "content" %}
        Obsah okna...
    {% endfill %}
{% endcomponent %}
```
Pro dynamické načítání použijte parametr `hx_url`.

## Integrace s Django Forms
Použijte `GovFormMixin` ve svých třídách formulářů:
```python
from sysnet_gov_django.forms import GovFormMixin
from django import forms

class MyForm(GovFormMixin, forms.Form):
    name = forms.CharField(label="Jméno")
```
Při renderování v šabloně:
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Alternativně renderujte pole přes gov_field -->
</form>
```

## Statické soubory
Knihovna očekává existenci následujících souborů ve složce `static/gov_django/`:
- `tokens.css`: Designové tokeny (barvy, spacing).
- `components.css`: Styly komponent.
- `main.js`: Interaktivita.

Tyto soubory jsou sdíleny s projektem `sysnet-gov-ui`.
