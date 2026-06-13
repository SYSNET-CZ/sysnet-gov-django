# Gap Analysis & Full Replacement Readiness Report: CITES-X vs ASYCUDA eCITES

## 1. Legislativní rigidita (Legislative Flexibility)
*   **Aktuální stav:** Systém CITES-X využívá validátor `CITESAppendix` definovaný jako Enum (I, II, III).
*   **Gap (Přílohy EU):** Nařízení (ES) č. 338/97 definuje přílohy A, B, C, D, které neodpovídají 1:1 CITES Appendices (např. populace přílohy II v příloze A).
*   **Flexibilita:** `CITESItem` obsahuje `extension_data` a `CITESPermit` také, což umožňuje ukládání národních/EU specifických parametrů. Nicméně, `CITESAppendix` Enum je příliš restriktivní pro EU legislativu.
*   **Doporučení:** Rozšířit `CITESAppendix` na `LegislationAppendix` s podporou prefixů (EU_A, EU_B, CITES_I) nebo implementovat mapovací vrstvu v pluginech `cites-portal-cz/sk`.

## 2. Bezpečnost a Neodvolatelnost (Non-repudiation)
*   **Aktuální stav:** Implementována `AuditLog` tabulka připravená pro TimescaleDB (hypertables) zajišťující výkonný logování. Implementován `EpixTranslator` s podporou `signxml` (XAdES-BES styl).
*   **Gap (Právní "průstřelnost"):**
    *   **Audit Log:** Aktuální implementace audit logu v `packages/cites-core-engine/sysnet_cites_core_engine/audit/models.py` nepoužívá kryptografické řetězení (hash chaining). Záznamy v TimescaleDB lze sice těžko smazat bez stop, ale nejsou matematicky nepopiratelné v případě kompromitace DB adminem.
    *   **XAdES:** Podpora v `EpixTranslator` je základní. Chybí XAdES-T (Timestamping) a XAdES-XL (Long-term validation) podpora, která je klíčová pro celní řízení trvající roky.
*   **Doporučení:** Integrovat RFC 3161 timestamping do procesu podpisu a implementovat Ledger hash-chaining (každý nový záznam obsahuje hash předchozího).

## 3. Integrace a Conflict Management (Sync)
*   **Aktuální stav:** `QuotaService` plánuje atomické operace (`check_and_reserve`). `LedgerEntry` obsahuje `mrn_number` pro linkování s celním řízením.
*   **Gap (Paralelní běh):** Neexistuje mechanismus pro externí synchronizaci kvót v reálném čase, pokud by část agendy běžela v ASYCUDA.
*   **Conflict Management:** Pokud ASYCUDA odečte kvótu, CITES-X to neuvidí bez aktivního pullu/webhooku.
*   **Doporučení:** Implementovat `QuotaSyncWorker`, který se periodicky dotazuje na stav globálních/národních kvót přes EPIX nebo národní celní rozhraní a řeší konflikty pomocí "Reservation Tokens".

## 4. Slabiny a Kritická místa
*   **Handling CA (Certifikátové autority):** `EpixTranslator` načítá klíče z environmentálních proměnných. Pro EPIX (G2G) je potřeba komplexní PKI management a handling "Trust Listů" cizích států.
*   **Offline režim:** Architektura FastAPI je silně závislá na online DB. Odlehlá celní pracoviště (v případě výpadku) nemají lokální cache pro validaci.
*   **Konfiskáty:** Workflow pro konfiskáty (změna vlastníka na stát, následný prodej/likvidace) není v modelech explicitně podchyceno. Chybí stav `CONFISCATED`.
*   **EPIX Gateway:** UN/CEFACT validace je označena jako "implementing" v `main.py`.

## Závěr: Replacement Readiness Score
**45% - PROTOTYPE STATUS.** 
CITES-X má robustní datové základy a moderní stack (PostGIS, TimescaleDB), ale postrádá "Enterprise-grade" bezpečnostní prvky (XAdES-T, Audit Chaining) a plnou podporu EU legislativních specifik, které jsou nezbytné pro plnohodnotnou náhradu ASYCUDA eCITES v EU prostředí.

---
Vytvořeno Hermes Agentem pro CITES-X Project.
