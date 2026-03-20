---
name: skill-openapi-modi
description: Creazione specifiche OpenAPI 3.0+ conformi alle Linee Guida AgID ModI (Modello di Interoperabilità) con arricchimento semantico JSON-LD. Include workflow completo con API Design Canvas, generazione automatica, validazione conformità e mappatura ontologie italiane (CPV, DCAT-AP_IT, CLV, COV). Usa questa skill quando l'utente chiede di creare specifiche OpenAPI per la PA italiana, menziona linee guida AgID, ModI, interoperabilità PA, o richiede conformità agli standard di interoperabilità italiani.
license: MIT
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: mfortini/skill-openapi-modi
# corpus-url: https://github.com/mfortini/skill-openapi-modi/blob/bf08b0df700f5e94ce56569cbadd42ed9dcb500f/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Skill: OpenAPI Conforme alle Linee Guida AgID ModI

## Trigger
Usa questa skill quando:
- L'utente chiede di creare una specifica OpenAPI per la PA italiana
- Si menzionano "linee guida AgID", "ModI", "interoperabilità PA"
- Si deve documentare un'API REST per enti pubblici italiani
- Si richiede conformità agli standard di interoperabilità italiani

## MCP Tools Disponibili

1. **API Canvas Design** — Progettazione iniziale (scopo, stakeholder, risorse, operazioni)
2. **OAS Checker MCP** — Validazione conformità AgID (naming, sicurezza, RFC 7807)
3. **schema-gov-it MCP** — Arricchimento semantico (ontologie italiane, vocabolari controllati)

## Workflow in 7 Fasi

### FASE 1: Progettazione con Canvas API
Raccogliere requisiti prima di scrivere YAML:
- **Chi**: stakeholder (cittadini, imprese, altre PA)
- **Cosa**: casi d'uso principali
- **Come**: risorse REST e operazioni
- **Perché**: obiettivi di business
- **Sicurezza**: JWT / OAuth2 / mTLS, ruoli
- **NFR**: volumi, tempi di risposta, rate limiting

Output: documento di design condiviso.

### FASE 2: Generazione Specifica OpenAPI
Trasformare il design in specifica conforme ModI:
1. Struttura base (info, servers, security) — vedi regole sezioni 1-4
2. Per ogni risorsa: path REST, operazioni CRUD, schemi dati
3. Pattern ModI: paginazione, filtri, errori RFC 7807, health check `/status`
4. Esempi request/response per OGNI operazione (vedi regole esempi)

**Regole esempi (obbligatorie)**:
- `example` per ogni `requestBody` (POST, PUT, PATCH)
- `example` per ogni response `2xx` con body
- Esempi errore nei `components/responses`
- Valori realistici: nomi italiani, CF validi, date ISO 8601 con timezone, UUID plausibili
- Coerenza request↔response: il dato inviato in POST deve tornare nella response
- Collezioni: almeno 2 item diversificati
- Enum: coprire almeno 2 valori diversi
- Usare `examples` (plurale) per operazioni con varianti significative (es. polling asincrono)

### FASE 3: Arricchimento Semantico con schema-gov-it MCP

Per ogni schema:

1. **Cerca tipo ontologico**: `search_concepts(keyword)` → `inspect_concept(uri)`
   - Se trovato → `x-jsonld-type` con prefisso compatto
   - Se non trovato → segnala gap, suggerisci tipo più vicino
2. **Mappa proprietà**: `list_properties(ontologyUri)` → `get_property_details(propertyUri)`
   - Definisci prefissi PRIMA, poi `prefisso:nome`
   - Se non trovata → prova sinonimi, ontologie alternative, segnala gap
3. **Verifica vocabolari controllati**: `list_vocabularies()` → `browse_vocabulary(schemeUri, keyword)`
   - Se trovato → referenzia con URI compatta + codice `skos:notation`
   - Se non trovato → segnala gap, suggerisci codifica locale documentata
4. **Arricchisci descrizioni**: se assente/solo in inglese/generica → proponi testo migliorato in italiano
5. **Report di copertura**: N proprietà mappate / N totali, gap identificati, descrizioni arricchite

**Efficienza MCP**: usare SEMPRE `keyword` e `limit`. Non scaricare interi vocabolari. Preferire `search_concepts` a esplorazioni generiche.

### FASE 3.5: Validazione Semantica via MCP (OBBLIGATORIA)

> **REGOLA CRITICA**: Non usare MAI una URI ontologica copiata da template senza verificarla con schema-gov-it MCP. I template sono un PUNTO DI PARTENZA, la fonte di verità sono le ontologie via MCP.

Per ogni mappatura:
1. `search_concepts(keyword="nome proprietà")`
2. Se trovata: `get_property_details(propertyUri)` → verifica domain/range
3. Se domain/range compatibili → usa nel context con prefisso
4. Se domain/range incompatibili → segnala, cerca alternativa
5. Se non trovata → segnala gap, cerca in ontologie alternative

Per ogni `x-jsonld-type`: `inspect_concept(uri)` → verifica che la classe esista.
Per ogni vocabolario: `list_vocabularies()` → verifica che il ConceptScheme esista.

Produrre report:
```
REPORT VALIDAZIONE SEMANTICA
URI verificate OK: N | URI inesistenti: N | Domain/range incompatibili: N | Gap: N
```

### FASE 4: Validazione con oas-checker-mcp
Verificare conformità AgID. Errori critici: Problem schema mancante, path non kebab-case, security scheme assente, /status mancante.

### FASE 5: Iterazione
Correggere errori → ri-validare → raffinare semantica → re-iterare fino a score ≥ 95%.

### FASE 6: Generazione Esempi JSON-LD
SOLO per schemi con `x-jsonld-context` contenente mappature di proprietà:
- `{schema}.json`: risposta JSON standard
- `{schema}.jsonld`: risposta JSON-LD con `@context` espanso

NON generare `.jsonld` per schemi senza `x-jsonld-context`. Proprietà senza mappatura non appaiono nel `.jsonld` — documentare gap nel README.

**Validazione** (eseguire via Bash):
```bash
test -d jsonld/.venv || (python3 -m venv jsonld/.venv && jsonld/.venv/bin/pip install -q pyld)
cd jsonld/ && .venv/bin/python3 -c "
from pyld import jsonld
import json, glob, sys
errors = 0
for f in sorted(glob.glob('*.jsonld')):
    try:
        with open(f) as fh:
            doc = json.load(fh)
        if '@context' not in doc:
            has_nested = any('@context' in v for v in doc.values() if isinstance(v, dict))
            if not has_nested:
                print(f'SKIP {f}: nessun @context (non e JSON-LD)')
                continue
        expanded = jsonld.expand(doc)
        n_triples = sum(len(node.keys()) - (1 if '@type' in node else 0) for node in expanded) if expanded else 0
        print(f'OK   {f} ({len(expanded)} nodi, ~{n_triples} proprieta espanse)')
    except json.JSONDecodeError as e:
        print(f'ERR  {f}: JSON non valido - {e}')
        errors += 1
    except Exception as e:
        print(f'ERR  {f}: {e}')
        errors += 1
sys.exit(1 if errors else 0)
"
```

### FASE 7: Generazione LOG.md
Genera `LOG.md` nella stessa directory del file OpenAPI con:
- Metadata (file, data, versione, azione)
- Fasi completate e decisioni di design
- Report semantico: ontologie usate, copertura per schema, mappature verificate, gap identificati, vocabolari controllati
- Istruzioni operative per ampliare/modificare le semantiche (personalizzate per l'API)
- Storico modifiche

Alla modifica di specifica esistente: aggiornare LOG.md (storico + copertura + gap risolti/nuovi).

---

## Regole OpenAPI ModI

### 1. Metadati Obbligatori (info)

Campi richiesti: `title`, `version` (semver), `description` (esaustiva), `contact` (name, url, email), `license` (CC BY 4.0), `x-api-id` (univoco), `x-summary` (max 80 char).

### 2. Server
- DEVE utilizzare HTTPS (TLS 1.2+)
- Versionamento nel path (`/v1`, `/v2`)
- Almeno ambienti test e produzione

### 3. Naming Convention Path
- Kebab-case, plurale per collezioni (`/documenti`), singolare per risorse (`/documenti/{id-documento}`)
- Evitare verbi nei path (usare metodi HTTP)

### 4. Metodi HTTP

| Metodo | Uso | Idempotente | Safe |
|--------|-----|:-----------:|:----:|
| GET | Lettura | ✓ | ✓ |
| POST | Creazione | ✗ | ✗ |
| PUT | Aggiornamento completo | ✓ | ✗ |
| PATCH | Aggiornamento parziale | ✗ | ✗ |
| DELETE | Eliminazione | ✓ | ✗ |

### 5. Codici di Risposta
Errori 4xx/5xx DEVONO usare `application/problem+json` con schema Problem (RFC 7807).
429 DEVE includere header `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.

### 6. Schema Problem (RFC 7807) — obbligatorio
```yaml
Problem:
  type: object
  required: [status, title]
  properties:
    type: {type: string, format: uri}
    status: {type: integer, format: int32}
    title: {type: string}
    detail: {type: string}
    instance: {type: string, format: uri}
```

### 7. Header Standard
- `X-Request-ID` (uuid): tracciamento richiesta
- `X-Correlation-ID` (uuid): correlazione richieste multiple
- `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`: rate limiting

### 8. Paginazione (per collezioni)
Query parameters: `limit` (1-100, default 20), `offset` (min 0, default 0), `cursor` (alternativo).
Response: oggetto con `items` (array), `count` (totale), `limit`, `offset`. Header `Link` per navigazione.

### 9. Filtri e Ricerca
Parametri standard: `q` (ricerca), `sort` (+asc/-desc), filtri per campo (stato, data_da, data_a).

### 10. Pattern di Sicurezza
DEVE implementare almeno uno:
- **ID_AUTH_REST_01**: Bearer Token JWT (`type: http, scheme: bearer, bearerFormat: JWT`)
- **ID_AUTH_REST_02**: OAuth2 (`type: oauth2, flows: clientCredentials`)

### 11. Tags
Raggruppare operazioni correlate. Usare `x-goal` per indicare lo scopo funzionale.

### 12. Pattern di Interazione

**BLOCK_REST** — sincrono (< 10s): POST → 200/201 con risultato.

**NONBLOCK_REST_PULL** — asincrono (> 10s): POST → 202 con `Location` header → GET polling su `/elaborazioni/{id}` con `stato` (IN_CORSO/COMPLETATA/ERRORE), `progresso` (0-100), `risultato`/`errore`.

### 13. Health Check — endpoint `/status` obbligatorio
Response: `status` (OK/DEGRADED/DOWN), `version`, `timestamp`.

---

## Regole JSON-LD e Semantica

### Principi Context
1. Definire prima TUTTI i prefissi necessari
2. `@vocab` sul namespace più usato nello schema
3. `@base` sull'URL base delle risorse
4. Mappare ogni proprietà con `prefisso:nome` — **mai URI complete**
5. Schemi senza corrispondenza ontologica (status, errori, metriche, wrapper): **NON aggiungere `x-jsonld-context`**. Usare commento YAML: `# x-jsonld: nessuna corrispondenza ontologica`
6. Context con soli prefissi senza mappature: **NON aggiungere**. I prefissi servono solo se usati.
7. Schemi contenitore con `$ref`: semantica delegata ai sotto-schemi.

### Prefissi Standard

| Prefisso | URI |
|----------|-----|
| CPV | `https://w3id.org/italia/onto/CPV/` |
| CLV | `https://w3id.org/italia/onto/CLV/` |
| COV | `https://w3id.org/italia/onto/COV/` |
| SM | `https://w3id.org/italia/onto/SM/` |
| TI | `https://w3id.org/italia/onto/TI/` |
| l0 | `https://w3id.org/italia/onto/l0/` |
| dct | `http://purl.org/dc/terms/` |
| dcat | `http://www.w3.org/ns/dcat#` |
| foaf | `http://xmlns.com/foaf/0.1/` |
| schema | `http://schema.org/` |
| org | `http://www.w3.org/ns/org#` |
| skos | `http://www.w3.org/2004/02/skos/core#` |
| xsd | `http://www.w3.org/2001/XMLSchema#` |

### Strategia Mapping con MCP

**Per ogni schema**:
1. Cerca tipo → `search_concepts` / `inspect_concept` → `x-jsonld-type`
2. Per ogni proprietà → `list_properties` / `get_property_details` → aggiungi al context
3. Per ogni enum → `list_vocabularies` / `browse_vocabulary` → referenzia vocabolario
4. Per ogni gap → prova sinonimi, ontologie alternative, documenta con suggerimento

**Tool MCP di riferimento**:

| Cosa cerco | Tool |
|-----------|------|
| Classe/tipo | `search_concepts(keyword)` → `inspect_concept(uri)` |
| Proprietà ontologia | `list_properties(ontologyUri)` |
| Dettaglio proprietà | `get_property_details(propertyUri)` |
| Vocabolario controllato | `list_vocabularies()` → `browse_vocabulary(schemeUri, keyword)` |
| Relazione tra concetti | `find_relations(sourceUri, targetUri)` |
| Lista ontologie | `list_ontologies()` → `explore_ontology(ontologyUri)` |
| Comuni/province | `list_municipalities(keyword)` / `list_provinces(keyword)` |

### Suggerimenti Proattivi per la Semantica

**Proprietà senza corrispondenza**: segnalare, suggerire alternative (schema.org, Dublin Core, FOAF), proporre estensione custom `https://w3id.org/italia/onto/{Ontologia}/{Nome}`, documentare gap con commento YAML.

**Descrizioni insufficienti**: se assente → proponi in italiano. Se solo inglese → traduci. Se generica → arricchisci con dettagli dominio PA.

**Enum senza vocabolario**: segnalare, suggerire il più vicino, proporre codifica locale documentata con riferimento a `https://github.com/italia/daf-ontologie-vocabolari-controllati`.

### Esempio Context Compatto (pattern da seguire)
```yaml
Persona:
  type: object
  x-jsonld-type: 'CPV:Person'
  x-jsonld-context:
    CPV: 'https://w3id.org/italia/onto/CPV/'
    foaf: 'http://xmlns.com/foaf/0.1/'
    '@vocab': 'https://w3id.org/italia/onto/CPV/'
    '@base': 'https://api.example.gov.it/v1/persone/'
    id: '@id'
    type: '@type'
    nome: 'CPV:givenName'
    cognome: 'CPV:familyName'
    codice-fiscale: 'CPV:taxCode'
    email: 'foaf:mbox'          # Gap CPV: fallback foaf
```

---

## Registro Correzioni Semantiche

Knowledge appresa da verifiche MCP. Consultare SEMPRE prima di mappare.

### Ultima verifica MCP: 2025-02-11

### Errori corretti

| Mappatura errata | Correzione | Motivo |
|---|---|---|
| `foaf:givenName` per nome persona | `CPV:givenName` | Proprietà nativa CPV con domain CPV:Person |
| `foaf:familyName` per cognome persona | `CPV:familyName` | Proprietà nativa CPV con domain CPV:Person |
| `schema:birthDate` per data nascita | `CPV:dateOfBirth` | Proprietà nativa CPV (range: xsd:dateTime) |
| `CPV:hasResidence` per residenza | `CPV:hasResidenceInTime` | `CPV:hasResidence` NON ESISTE; range: CPV:ResidenceInTime |
| `foaf:gender` per sesso | `CPV:hasSex` | ObjectProperty CPV con range CPV:Sex |
| `CLV:streetNumber` per numero civico | `CLV:hasNumber` | ObjectProperty con range CLV:CivicNumbering |
| `CLV:cityName` per nome comune | `rdfs:label` o `skos:prefLabel` | `CLV:cityName` NON ESISTE in CLV |
| `CLV:code` per codice ISTAT | `CLV:hasIdentifier` | ObjectProperty con range CLV:Identifier |
| `dct:title` per nome organizzazione | `COV:legalName` | Proprietà nativa COV con domain COV:Organization |
| `COV:taxCode` per partita IVA | `COV:VATnumber` | `COV:taxCode` è per il codice fiscale organizzazione, non la P.IVA |
| `foaf:Person` come tipo | `CPV:Person` | Usare ontologia nativa italiana per contesto PA |
| `foaf:firstName`/`foaf:lastName` | `CPV:givenName`/`CPV:familyName` | `foaf:firstName` e `foaf:lastName` non sono standard FOAF |

### Gap semantici noti

| Proprietà | Ontologia attesa | Stato | Note |
|---|---|---|---|
| CAP (codice postale) | CLV | ASSENTE | `CLV:postCode` non esiste. Nessuna alternativa. |
| Stato civile | CPV | ASSENTE | `CPV:hasMaritalStatus` non esiste. |
| Email (persona) | CPV | GAP | Fallback: `foaf:mbox` |
| Telefono (persona) | CPV | GAP | Fallback: `foaf:phone` |
| Email (organizzazione) | COV | ASSENTE | Alternativa: `SM:emailAddress` (domain: SM:Email) |
| PEC (organizzazione) | COV | ASSENTE | Nessuna proprietà standard per PEC |

### Proprietà con range complesso (ObjectProperty vs valore semplice)

Nelle API REST si rappresentano come valori semplici, ma ontologicamente sono ObjectProperty:

| Proprietà | Range | Nota API |
|---|---|---|
| `CLV:hasNumber` | CLV:CivicNumbering | Si usa il valore testuale |
| `CLV:hasProvince` | CLV:Province | Si usa la sigla (es. "RM") |
| `CLV:hasRegion` | CLV:Region | Si usa il nome (es. "Lazio") |
| `CLV:hasIdentifier` | CLV:Identifier | Si usa il codice ISTAT diretto |
| `CPV:hasSex` | CPV:Sex | Si usa un enum (M/F/X) |
| `CPV:hasResidenceInTime` | CPV:ResidenceInTime | Pattern n-ario per storico residenze |

### Mappature di riferimento per entità comuni PA

**Persona** → `x-jsonld-type: 'CPV:Person'`
- nome → `CPV:givenName` (DatatypeProperty, range: xsd:string)
- cognome → `CPV:familyName` (DatatypeProperty Functional, range: xsd:string)
- codice-fiscale → `CPV:taxCode`
- data-nascita → `CPV:dateOfBirth` (DatatypeProperty Functional, range: xsd:dateTime)
- email → `foaf:mbox` (gap CPV)
- telefono → `foaf:phone` (gap CPV)

**Indirizzo** → `x-jsonld-type: 'CLV:Address'`
- via → `CLV:fullAddress` (DatatypeProperty Functional, range: Literal)
- civico → `CLV:hasNumber` (ObjectProperty, range: CLV:CivicNumbering)
- cap → GAP SEMANTICO (CLV:postCode non esiste)
- comune → `CLV:hasCity` (ObjectProperty, range: CLV:City)
- provincia → `CLV:hasProvince` (ObjectProperty, range: CLV:Province)
- regione → `CLV:hasRegion` (ObjectProperty, range: CLV:Region)

**Organizzazione** → `x-jsonld-type: 'COV:Organization'`
- nome → `COV:legalName` (DatatypeProperty, range: Literal)
- codice-ipa → `COV:IPAcode`
- partita-iva → `COV:VATnumber` (DatatypeProperty Functional — NON è COV:taxCode!)
- email → GAP (alternativa: `SM:emailAddress`)
- pec → GAP (nessuna proprietà standard)
- indirizzo → `CLV:hasAddress`

**Documento Amministrativo** → `x-jsonld-type: 'CPV:Document'`
- identificativo → `dct:identifier`
- titolo → `dct:title`
- descrizione → `dct:description`
- tipo/formato → `dct:type` / `dct:format`
- date creazione/modifica → `dct:created` / `dct:modified`
- autore/editore → `dct:creator` / `dct:publisher`

---

## Checklist di Conformità

### Struttura e Conformità
- [ ] OpenAPI 3.0.3+
- [ ] Info block completo (title, version, description, contact, x-api-id, x-summary)
- [ ] HTTPS, path kebab-case, metodi HTTP corretti
- [ ] Errori 4xx/5xx con schema Problem (RFC 7807)
- [ ] Endpoint /status, security scheme, rate limiting headers
- [ ] Paginazione per collezioni, X-Request-ID
- [ ] Esempi request per ogni POST/PUT/PATCH, esempi response per ogni 2xx
- [ ] Esempi coerenti request↔response, valori realistici, collezioni con ≥2 item
- [ ] Descrizioni chiare in italiano, pattern validation per CF/P.IVA, date ISO 8601

### Semantica e JSON-LD
- [ ] OGNI URI ontologica verificata via MCP — MAI copiare da template senza verificare
- [ ] Context con prefissi compatti (no URI espanse), `@vocab` e `@base` definiti
- [ ] `x-jsonld-type` con prefisso per ogni schema principale
- [ ] Domain/range verificati compatibili
- [ ] Gap segnalati nelle description con suggerimento alternativo
- [ ] Report copertura semantica + report validazione semantica (FASE 3.5)

### JSON-LD (se generati)
- [ ] File `.jsonld` solo per schemi con `x-jsonld-context` con mappature reali
- [ ] `@context` presente con mappature, tutti i prefissi definiti
- [ ] Espansione produce URI valide, `@type` presente
- [ ] Gap documentati nel README

---

## Template Base (Appendice)

```yaml
openapi: 3.0.3
info:
  title: API [Nome Servizio]
  version: 1.0.0
  description: |
    [Descrizione dettagliata]
    ## Scopo
    [Spiegare lo scopo]
    ## Funzionalità
    - [Funzionalità 1]
  contact:
    name: [Nome Ufficio]
    email: [email]@[ente].gov.it
    url: https://[ente].gov.it
  license:
    name: CC BY 4.0
    url: https://creativecommons.org/licenses/by/4.0/
  x-api-id: [identificativo-univoco]
  x-summary: [Descrizione breve max 80 caratteri]

servers:
  - url: https://api.[ente].gov.it/v1
    description: Produzione
  - url: https://api-test.[ente].gov.it/v1
    description: Test

tags:
  - name: [Categoria1]
    description: [Descrizione]
    x-goal: [Obiettivo funzionale]

paths:
  /status:
    get:
      summary: Health check
      operationId: getStatus
      tags: [System]
      responses:
        '200':
          description: Servizio operativo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/StatusResponse'
        '503':
          description: Servizio non disponibile

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: Token JWT per autenticazione

  schemas:
    Problem:
      type: object
      required: [status, title]
      properties:
        type: {type: string, format: uri}
        status: {type: integer, format: int32}
        title: {type: string}
        detail: {type: string}
        instance: {type: string, format: uri}

    StatusResponse:
      # x-jsonld: nessuna corrispondenza ontologica (schema tecnico)
      type: object
      properties:
        status: {type: string, enum: [OK, DEGRADED, DOWN]}
        version: {type: string}
        timestamp: {type: string, format: date-time}

  responses:
    BadRequest:
      description: Richiesta non valida
      content:
        application/problem+json:
          schema: {$ref: '#/components/schemas/Problem'}
    Unauthorized:
      description: Non autenticato
      content:
        application/problem+json:
          schema: {$ref: '#/components/schemas/Problem'}
    Forbidden:
      description: Non autorizzato
      content:
        application/problem+json:
          schema: {$ref: '#/components/schemas/Problem'}
    NotFound:
      description: Risorsa non trovata
      content:
        application/problem+json:
          schema: {$ref: '#/components/schemas/Problem'}
    TooManyRequests:
      description: Troppe richieste
      headers:
        X-RateLimit-Limit: {schema: {type: integer}}
        X-RateLimit-Remaining: {schema: {type: integer}}
        Retry-After: {schema: {type: integer}}
      content:
        application/problem+json:
          schema: {$ref: '#/components/schemas/Problem'}
    InternalServerError:
      description: Errore interno del server
      content:
        application/problem+json:
          schema: {$ref: '#/components/schemas/Problem'}

security:
  - bearerAuth: []
```

---

## Riferimenti

- [Linee Guida Interoperabilità Tecnica PA](https://www.agid.gov.it/it/infrastrutture/sistema-pubblico-connettivita/il-nuovo-modello-interoperabilita)
- [Pattern di Interazione](https://docs.italia.it/italia/piano-triennale-ict/lg-modellointeroperabilita-docs/)
- [Pattern di Sicurezza](https://www.agid.gov.it/sites/agid/files/2024-05/linee_guida_tecnologie_e_standard_sicurezza_interoperabilit_api_sistemi_informatici.pdf)
- [RFC 7807 - Problem Details](https://www.rfc-editor.org/rfc/rfc7807)
- [Vocabolari Controllati AgID](https://github.com/italia/daf-ontologie-vocabolari-controllati)
- [api-oas-checker (Spectral ruleset AgID)](https://github.com/teamdigitale/api-oas-checker)