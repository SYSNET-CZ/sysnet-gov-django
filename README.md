# SYSNET Gov UI — Design System Boilerplate

Moderní, výkonná a legislativně čistá knihovna Vue 3 komponent pro aplikace české státní správy. Vzniklo jako náhrada za GDS v4 (ADR-004) s cílem eliminovat technický dluh a poskytnout špičkový vývojářský zážitek.

## 🛠 Technologický Stack
- **Framework:** Vue 3.5+ (Composition API, `<script setup>`)
- **Jazyk:** TypeScript (striktní typování)
- **Styling:** Tailwind CSS v4 (Nativní CSS proměnné, zero-runtime overhead)
- **Ikony:** Lucide Vue Next (zapouzdřeno v `GovIcon`)
- **Build Tool:** Vite (ESM exporty, HMR)
- **Dokumentace:** Storybook 8

## 🎨 Design Tokeny
Knihovna striktně dodržuje barevnou paletu Jednotného vizuálního stylu (JVS):
- `gov-blue-primary`: `#00469B` (Hlavní akční barva)
- `gov-blue-dark`: `#0C1838` (Typografie a dark prvky)
- `gov-error`: `#D70C0F` (Chybové stavy)
- `gov-bg-gray`: `#F2F6FC` (Pozadí aplikací)

## ♿️ Přístupnost (A11y)
Všechny komponenty jsou navrženy s ohledem na zákon 99/2019 Sb.:
- Automatické generování unikátních ID (`useId`)
- Vazby `aria-describedby` pro spojení chybových hlášek s poli
- Jasně definovaný focus ring (`gov-blue-light`) pro navigaci klávesnicí
- Sémantické HTML tagy

## 🚀 Komponenty v MVP v0.1.0
- **Layout:** `GovHeader` (s logem), `GovSidebar` (navigace), `GovCard` (kontejnery)
- **Formuláře:** `GovInput`, `GovSelect`, `GovField` (validace wrapper)
- **Základní:** `GovButton`, `GovIcon` (Lucide wrapper), `GovLogo` (JVS loga MŽP/MZe)
- **Data & Feedback:** `GovTable` (čistý výpis dat), `GovAlert` (notifikace)

## 🏗 Instalace a použití
Pro lokální vývoj v monorepu:
```bash
npm install @sysnet-cz/gov-ui
```

Import v aplikaci:
```ts
import { GovButton, GovHeader } from '@sysnet-cz/gov-ui';
import '@sysnet-cz/gov-ui/style.css';
```

---
© 2024 SYSNET s.r.o. — Vyvinuto pro projekty SEVESO, SEKM a DCO.
