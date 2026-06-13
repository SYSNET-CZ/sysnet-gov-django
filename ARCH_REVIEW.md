# Architektonická revize a Akční plán CITES-X (2026)

## 1. Identifikované kritické nálezy

### 1.1 Legislativa a Provozní integrita
- **Absence hlídání lhůt (SLA):** Systém postrádá logiku pro eskalační mechanismy (např. 30denní lhůta pro vědecký orgán).
- **Validace v reálném čase:** Chybí vynucená kontrola `expiry_date` a `status == ACTIVE` během procesu `deduct` v Ledgeru.
- **GDPR a retence:** Osobní údaje (CITESPerson) nejsou anonymizovány po uplynutí skartační lhůty (10 let).

### 1.2 Kompatibilita s ASYCUDA (UNCTAD)
- **Quota Management:** Chybí evidence národních/globálních exportních kvót. Bez toho nelze systém integrovat do celního ekosystému.
- **Atomický Handshake:** Chybí dvoufázové potvrzení odpisů (Reservation -> Confirmation) navázané na MRN (Movement Reference Number).
- **Data Model:** V modelech chybí HS kódy (Harmonized System) a standardní ISO validace.

### 1.3 Technické a bezpečnostní dluhy
- **Duplicity:** Model `LedgerEntry` je definován redundantně v engine i types.
- **EPIX Security:** XML parser v EPIX gateway je náchylný na XXE (XML External Entity) útoky.
- **Auditní integrita:** IP adresa v logu TimescaleDB není vynucená.

---

## 2. Akční plán nápravy (H1-2026)

### Fáze A: Strukturální konsolidace (OKAMŽITĚ)
- **Úkol 1:** Přesun všech definic modelů (vč. LedgerEntry, Movement) do `cites-core-types`.
- **Úkol 2:** Oprava překlepu `mrd_number` -> `mrn_number` v celém codebase a přidání DB indexů.
- **Úkol 3:** Fix XXE vulnerability v `translator.py`.

### Fáze B: Quota & Validation Engine (STŘEDNĚDOBĚ)
- **Úkol 1:** Implementace `CITESQuota` modelu a služby `QuotaService`.
- **Úkol 2:** Rozšíření `CITESItem` o `hs_code`.
- **Úkol 3:** Upgrade `LedgerService.log()` o mandatory validation bucket (IsActive + IsNotExpired + HasQuota).

### Fáze C: ASYCUDA Gateway (PRODUKCE)
- **Úkol 1:** Implementace endpointu `/reserve` pro celní správu.
- **Úkol 2:** Implementace asynchronního potvrzování odpisů.
- **Úkol 3:** Integrace SLAWatcheru pro sledování lhůt v workflow.

---
*Schváleno: Hermes (AI Agent) na pokyn Radima Jägera.*
