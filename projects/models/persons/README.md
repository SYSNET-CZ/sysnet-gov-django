# sysnet-persons-model

Data model pro entity a osoby v ekosystému SYSNET. Postaveno na Pydantic v2.

## Instalace

```bash
pip install sysnet-persons-model
```

## Hlavní vlastnosti
- Podpora pro fyzické osoby (`IndividualType`) i právnické subjekty (`PersonEntityType`).
- Integrace s číselníky RPP (právní formy).
- Standardizovaná metadata životního cyklu (vytvoření, modifikace, smazání).
- **Opaque extension slot** (`agenda`) pro agendově specifická data.

## Verze
- **1.2.8**: Přidání atributu `agenda` (opaque extension slot) do `IndividualBaseType` a `PersonEntityBaseType`. Viz [AGENDA_GUIDE.md](docs/AGENDA_GUIDE.md).
- **1.2.7**: Přidání aliasu `metadata` pro pole `document` (Redmine #9850).
- **1.2.5**: Přidání `ScopeType` pro definici rozsahu působnosti subjektu.
- **1.1.2**: Původní stabilní verze s podporou Pydantic v2.

## Použití atributu agenda
Atribut `agenda` slouží pro data specifická pro konkrétní aplikace (HNVO, IPPC, CITES), která nepatří do společného jádra.

```python
# Příklad čtení dat pro agendu HNVO
hnvo_data = person.agenda.get("hnvo", {})
```
Podrobnosti naleznete v [dokumentaci k agendám](docs/AGENDA_GUIDE.md).
