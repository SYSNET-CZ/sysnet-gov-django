# Gap Analysis & Full Replacement Readiness Report (CITES-X)

## 1. Kritické rozdíly vs. UNCTAD ASYCUDA / ePERMIT

### 1.1 Právní neprůstřelnost (Non-repudiation)
- **Nález:** Současný auditní log v TimescaleDB je náchylný k manipulaci administrátorem.
- **Požadavek:** Zavedení kryptografického řetězení (Hash-chaining) každého záznamu na předchozí.
- **Status:** KRITICKÝ DLUH.

### 1.2 Legislativní flexibilita (EU vs. UN)
- **Nález:** Systém fixně používá UN Appendices (I, II, III).
- **Požadavek:** Nutnost podpory EU Annexes (A, B, C, D) se specifickou validací pro Přílohu A (high-level ochrana).
- **Status:** KRITICKÝ DLUH.

### 1.3 Digitální certifikace (XAdES-T)
- **Nález:** EPIX gateway používá pouze XAdES-BES (bez časového razítka).
- **Požadavek:** Upgrade na XAdES-T pro prokázání času podpisu po vypršení platnosti certifikátu.
- **Status:** STŘEDNÍ RIZIKO.

### 1.4 Operační kontinuita (Offline Mode)
- **Nález:** 100% závislost na online API.
- **Požadavek:** Lokální cache / synchronizační mechanismus pro celnice s výpadky spojení.
- **Status:** OPERAČNÍ RIZIKO.

---

## 2. Akční plán pro plnou náhradu (Full Replacement Plan)

### Krok 1: Kryptografický Audit (Immutable Ledger)
- Implementace tabulky `audit_chain` s poli `hash` a `prev_hash`.
- Každá akce (ACCESS, DEDUCT) vygeneruje SHA-256 hash, který sváže záznam s historií.

### Krok 2: Legislativní Mapping Layer
- Refaktoring `CITESAppendix` na `LegislationAppendix`.
- Implementace validační logiky: Pokud `Annex == A`, pak je odpis možný pouze s explicitním povolením k výjimce ze zákazu obchodních činností.

### Krok 3: EPIX PKI & Timestamping
- Integrace služby pro certifikované časové razítko (TSA).
- Implementace úložiště důvěryhodných certifikátů (`trust-store`) pro verifikaci zahraničních vlád.

---
*Zpracoval: Hermes (AI Agent) / 2026-06-13*
