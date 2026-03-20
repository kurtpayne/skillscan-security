---
name: grant-monitor
description: Monitor research grant opportunities and funding calls in epidemiology, dengue, global health, and AI for science. Automatically checks FAPESP, CNPq, NIH, Wellcome Trust portals for new editais and alerts about deadlines. Use when user asks about finding grants, editais de pesquisa, funding opportunities, or wants to track research funding calls.
# corpus-label: benign
# corpus-source: github-scrape-r3
# corpus-repo: fccoelho/grant-monitor
# corpus-url: https://github.com/fccoelho/grant-monitor/blob/7545bb398612cf6623020bdc98cd2e224cb56ecc/SKILL.md
# corpus-round: 2026-03-20
# corpus-format: markdown_fm
---

# Grant Monitor

Monitors research funding opportunities for:
- Epidemiology and dengue research
- Global health and public health
- AI for science and health
- Infectious disease surveillance
- Mathematical modeling and data science

## Supported Portals

### 🇧🇷 Brazilian
- **FAPESP** - Fundação de Amparo à Pesquisa do Estado de SP
- **CNPq** - Conselho Nacional de Desenvolvimento Científico
- **FAPERJ** - Fundação Carlos Chagas Filho (RJ)
- **FAPEMIG** - Fundação de Amparo à Pesquisa de Minas Gerais

### 🌍 International
- **NIH** - National Institutes of Health (EUA)
- **Wellcome Trust** - Global health research (UK)
- **ERC** - European Research Council
- **Bill & Melinda Gates Foundation** - Global health

### 🇨🇳 China
- **NSFC** - National Natural Science Foundation of China (国家自然科学基金委员会)
- **MOST** - Ministry of Science and Technology (科学技术部)
- **CAS** - Chinese Academy of Sciences (中国科学院)
- **Belt and Road Initiative** - International cooperation programs
- **CMB** - China Medical Board (funding for health research)

## Quick Start

### Check Specific Portal
```bash
# Check FAPESP for dengue/epidemiology editais
python scripts/check_fapesp.py --keywords "dengue,epidemiologia,arboviroses,saúde pública"

# Check CNPq
python scripts/check_cnpq.py --keywords "dengue,doenças infecciosas"

# Check NIH
python scripts/check_nih.py --keywords "dengue,epidemiology,arboviral"
```

### Check All Portals
```bash
python scripts/check_all.py --keywords "dengue,epidemiologia"
```

### Add Monitoring Job
```bash
# Weekly check (Mondays 9h)
python scripts/schedule_monitor.py --frequency weekly --day monday --time 09:00

# Daily check
python scripts/schedule_monitor.py --frequency daily --time 08:00
```

## View Tracked Grants

The system maintains a local database of tracked grants at:
`~/.nanobot/workspace/grant-monitor/grants.db`

### List Active Grants
```bash
python scripts/list_grants.py --status open
```

### Check Deadlines
```bash
python scripts/check_deadlines.py --days 30  # Shows grants closing in 30 days
```

## Grant Database Schema

See [references/database-schema.md](references/database-schema.md) for full schema.

Key fields:
- `portal`: Source portal (fapesp, cnpq, nih, etc.)
- `title`: Grant title
- `description`: Brief description
- `deadline`: Submission deadline (ISO 8601)
- `url`: Link to full edital
- `status`: open/closed/upcoming
- `keywords`: Matched keywords
- `eligibility`: Who can apply
- `amount`: Funding amount (when available)

## Adding New Keywords

Edit `references/keywords.txt` to add search terms.

### Current Keyword Categories:

**Epidemiology & Disease:**
- dengue, epidemiologia, epidemiology
- arboviroses, arboviral, zika, chikungunya
- doenças infecciosas, infectious diseases
- vigilância epidemiológica, disease surveillance
- transmissão de doenças, disease transmission

**Global Health:**
- global health, saúde global, international health
- one health, planetary health
- saúde pública, public health
- health systems, sistemas de saúde
- digital health, saúde digital, mHealth, telemedicine

**AI for Science:**
- artificial intelligence, inteligência artificial
- AI for science, AI for health
- machine learning, aprendizado de máquina
- deep learning, redes neurais, neural networks
- computational biology, bioinformatics
- data science, ciência de dados
- predictive modeling, modelagem preditiva

**Methods:**
- modelagem matemática, mathematical modeling
- bioestatística, biostatistics
- forecasting, previsão
- sistemas de informação em saúde, health information systems

## Manual Portal Checks

When web search is unavailable, guide user to:

### 🇧🇷 Brazil
1. **FAPESP**: https://fapesp.br/oportunidades/
2. **CNPq**: https://www.gov.br/cnpq/pt-br/edicitais

### 🌍 International
3. **NIH**: https://grants.nih.gov/funding/searchguide/index.html
4. **Wellcome**: https://wellcome.org/grant-funding/schemes

### 🇨🇳 China
5. **NSFC**: https://www.nsfc.gov.cn/ (English: https://www.nsfc.gov.cn/english/)
6. **MOST Programs**: http://www.most.gov.cn/
7. **CAS**: https://www.cas.cn/
8. **China Medical Board**: https://www.chinamedicalboard.org/funding-opportunities