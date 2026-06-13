# Contabo API Research

Detailní rešerše Contabo REST API v1.

## 1. Compute (Výpočetní zdroje)

Tento celek slouží ke správě VPS, VDS a dedikovaných serverů.

### Compute Instances
- **Klíčové endpointy:**
    - `GET /compute/instances`: Seznam všech instancí.
    - `POST /compute/instances`: Vytvoření nové instance (vyžaduje `productId`).
    - `GET /compute/instances/{instanceId}`: Detail konkrétní instance.
    - `PATCH /compute/instances/{instanceId}`: Aktualizace instance (např. tagy, jméno).
- **Možnosti:** Získání IP adres (IPv4/IPv6), stavu (running, stopped), regionu a konfigurace.

### Instance Actions
- **Klíčové endpointy:**
    - `POST /compute/instances/{instanceId}/actions/restart`: Restart serveru.
    - `POST /compute/instances/{instanceId}/actions/stop`: Vypnutí.
    - `POST /compute/instances/{instanceId}/actions/start`: Zapnutí.
    - `POST /compute/instances/{instanceId}/actions/reinstall`: Reinstalace (vyžaduje `imageId`).
- **Možnosti:** Ovládání životního cyklu serveru.

### Snapshots
- **Klíčové endpointy:**
    - `GET /compute/instances/{instanceId}/snapshots`: Seznam snapshotů.
    - `POST /compute/instances/{instanceId}/snapshots`: Vytvoření snapshotu.
    - `DELETE /compute/instances/{instanceId}/snapshots/{snapshotId}`: Smazání snapshotu.
    - `POST /compute/instances/{instanceId}/snapshots/{snapshotId}/rollback`: Obnova ze snapshotu.
- **Možnosti:** Zálohování a rychlá obnova stavu disku.

### Compute Images
- **Klíčové endpointy:**
    - `GET /compute/images`: Seznam dostupných images (vlastní i oficiální).
    - `POST /compute/images`: Vytvoření vlastního image.
- **Možnosti:** Správa operačních systémů pro instalaci.

---

## 2. Storage (Úložiště)

### Object Storage (S3 kompatibilní)
- **Klíčové endpointy:**
    - `GET /object-storages`: Výpis storage unit.
    - `POST /object-storages`: Vytvoření nové unit.
    - `GET /object-storages/{objectStorageId}`: Detail jednotky.
    - `GET /users/{userId}/object-storage-credentials`: Správa S3 klíčů.
- **Možnosti:** S3 kompatibilní úložiště pro data, zálohy a statický obsah.

---

## 3. Network (Síťování)

### Private Networks (VPC)
- **Klíčové endpointy:**
    - `GET /private-networks`: Seznam privátních sítí.
    - `POST /private-networks`: Vytvoření privátní sítě.
    - `POST /private-networks/{privateNetworkId}/instances/{instanceId}`: Přidání instance do sítě.
- **Možnosti:** Propojení serverů přes privátní rozhraní (izolované od internetu).

### VIP (Virtual IP)
- **Klíčové endpointy:**
    - `GET /network/vips`: Správa virtuálních IP adres.
- **Možnosti:** Failover řešení a high availability.

---

## 4. Security (Zabezpečení a přístup)

### Secrets (Hesla a SSH klíče)
- **Klíčové endpointy:**
    - `GET /secrets`: Seznam uložených secretů.
    - `POST /secrets`: Uložení nového SSH klíče nebo hesla.
- **Možnosti:** Centrální správa SSH klíčů pro automatizované nasazení.

### Firewalls
- **Klíčové endpointy:**
    - `GET /firewalls`: Seznam firewall pravidel.
    - `POST /firewalls`: Vytvoření firewallu.
    - `PATCH /firewalls/{firewallId}`: Úprava pravidel.
- **Možnosti:** L3/L4 filtrování provozu před dosažením instance.

### IAM (Users & Roles)
- **Klíčové endpointy:**
    - `GET /users`: Správa uživatelských účtů.
    - `GET /roles`: Role-based access control (RBAC).
- **Možnosti:** Delegování přístupu k API pro různé členy týmu.

---

## 5. Admin & Management

### Domains & DNS
- **Klíčové endpointy:**
    - `GET /domains`: Registrace a správa domén.
    - `GET /dns`: Kompletní správa DNS zón a záznamů (A, MX, TXT atd.).
- **Možnosti:** Plná automatizace správy DNS záznamů.

### Tags
- **Klíčové endpointy:**
    - `GET /tags`: Seznam tagů.
    - `POST /tags/assignments`: Přiřazení tagu k prostředku (instance, image, atd.).
- **Možnosti:** Logické organizování a filtrování zdrojů.

### Audits
- **Klíčové endpointy:**
    - `/compute/instances/audits`
    - `/object-storages/audits`
    - `/firewalls/audits`
- **Možnosti:** Sledování historie změn a akcí provedených přes API.

### Troubleshooting
- **Klíčové endpointy:**
    - `GET /troubleshooting/checks`: Monitoring a health checky.
- **Možnosti:** Diagnostika stavu služeb.
