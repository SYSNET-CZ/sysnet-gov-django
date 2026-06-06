#!/usr/bin/env python3
import shutil
from pathlib import Path

# Cesty k projektům
PROJECT_ROOT = Path(__file__).resolve().parent.parent
UI_PROJECT = PROJECT_ROOT.parent / "sysnet-gov-ui"
STATIC_ROOT = PROJECT_ROOT / "sysnet_gov_django" / "static" / "gov_django"

def sync_assets():
    print(f"🔄 Synchronizace assetů z sysnet-gov-ui...")
    
    if not UI_PROJECT.exists():
        print(f"❌ Chyba: Projekt sysnet-gov-ui nebyl nalezen v {UI_PROJECT}")
        return

    # Mapování souborů: (zdroj v UI -> cíl v Django lib)
    # Předpoklad: UI projekt má buildované CSS/JS nebo linkujeme na zdrojové tokeny
    mapping = {
        UI_PROJECT / "src" / "assets" / "css" / "tokens.css": STATIC_ROOT / "css" / "tokens.css",
        # Sem přidáme další soubory po buildu UI (dist/assets/...)
    }

    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
    (STATIC_ROOT / "css").mkdir(exist_ok=True)
    (STATIC_ROOT / "js").mkdir(exist_ok=True)

    for src, dst in mapping.items():
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ Zkopírováno: {src.name} -> {dst}")
        else:
            print(f"⚠️ Varování: Soubor {src} neexistuje.")

    # Vytvoření placeholderů pro chybějící soubory, aby build neselhal
    for missing in ["css/components.css", "js/main.js"]:
        f = STATIC_ROOT / missing
        if not f.exists():
            f.write_text("/* Placeholder */")
            print(f"📝 Vytvořen placeholder: {missing}")

if __name__ == "__main__":
    sync_assets()
