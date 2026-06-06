from django.urls import path
from django.shortcuts import render

def index(request):
    menu = [
        {"label": "Nástěnka", "url": "#", "active": True, "icon": "home"},
        {"label": "Uživatelé", "url": "#", "active": False, "icon": "users"},
        {"label": "Nastavení", "url": "#", "active": False, "icon": "settings"},
    ]
    
    breadcrumbs = [
        {"label": "Domů", "url": "/"},
        {"label": "Komponenty", "url": "/"},
        {"label": "Styleguide", "url": "#"},
    ]

    table_headers = ["ID", "Název", "Status", "Akce"]
    table_rows = [
        ["1", "Žádost o dotaci", "V řešení", "Detail"],
        ["2", "Oprava chodníku", "Odesláno", "Detail"],
    ]

    return render(request, "index.html", {
        "menu": menu,
        "breadcrumbs": breadcrumbs,
        "table_headers": table_headers,
        "table_rows": table_rows
    })

urlpatterns = [
    path('', index, name='index'),
]
